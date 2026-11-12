#!/usr/bin/env python3
"""
Canvas Course Sync for MSQE_Stuff
Scrapes Canvas LMS via active Arc browser session, identifies course differentials,
downloads newly published files into the appropriate course directories, and
optionally commits and pushes according to AGENTS.md rules.
"""

import os
import sys
import json
import time
import base64
import re
import shutil
import hashlib
import argparse
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlsplit

REPO_ROOT = str(Path(__file__).resolve().parents[1])
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
CANVAS_ORIGIN = "https://canvas.calpoly.edu"
API_CACHE = {}
SCAN_WARNINGS = set()

COURSE_MAP = {
    192233: "SS1-ECON5015-ComputingMLEcon",
    194701: "SS1-ECON5021-AdvEconometrics1",
    193727: "SS1-ECON5030-MicroeconomicAnalysis",
    192053: "SS1-ECON5040-DynamicStochasticModeling",
    192663: "SS1-ECON5560-AppliedEconProj1",
    197333: "EXT/Graduate_Student_Materials",
    185611: "SP26-ECON470-MicroeconAI",
    187003: "SU26-GSE510-MathEcon"
}

# ----------------------------------------------------------------------
# Browser Communication (Arc AppleScript)
# ----------------------------------------------------------------------

# Arc runs each AppleScript `execute` on its main thread and waits for the page's
# answer, so every call must return at once: requests run as async fetches in the
# page and are polled with tiny evals. A synchronous XHR here freezes all of Arc.
# The tab is addressed by id and never selected, so it can stay in the background.
CANVAS_TAB = {}
POLL_SECONDS = 0.25
CHUNK_CHARS = 512 * 1024
JOB_TIMEOUT = 300


def find_canvas_tab():
    """Find a signed-in Canvas tab in Arc and remember it, without selecting it."""
    applescript = '''
    tell application "Arc"
        repeat with w in windows
            try
                if (URL of active tab of w) starts with "https://canvas.calpoly.edu" then
                    return (id of w) & " " & (id of active tab of w) & " " & (URL of active tab of w)
                end if
            end try
        end repeat
        repeat with w in windows
            repeat with t in tabs of w
                try
                    if (URL of t) starts with "https://canvas.calpoly.edu" then
                        return (id of w) & " " & (id of t) & " " & (URL of t)
                    end if
                end try
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    p = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, timeout=20)
    if p.returncode:
        raise RuntimeError("Could not inspect Arc's Canvas tab: " + p.stderr.strip())
    parts = p.stdout.strip().split(" ", 2)
    if len(parts) != 3:
        CANVAS_TAB.clear()
        return "NOT_FOUND"
    CANVAS_TAB.update(window=parts[0], tab=parts[1])
    return parts[2]


def arc_eval(js_code):
    """Run a short JavaScript expression in the remembered Canvas tab."""
    if not CANVAS_TAB and "NOT_FOUND" in find_canvas_tab():
        raise RuntimeError("The Canvas tab in Arc was closed; scan is incomplete.")
    escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    for attempt in range(2):
        applescript = (f'tell application "Arc" to return (execute (tab id "{CANVAS_TAB["tab"]}" '
                       f'of window id "{CANVAS_TAB["window"]}") javascript "{escaped_js}")')
        p = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, timeout=30)
        if p.returncode == 0:
            break
        # The tab may have moved windows or been closed; look for it once more.
        if attempt or "NOT_FOUND" in find_canvas_tab():
            raise RuntimeError(f"AppleScript error: {p.stderr.strip()}")
    res = p.stdout.strip()
    if res.startswith('"') and res.endswith('"'):
        try:
            res = json.loads(res)
        except Exception:
            pass
    return res


def browser_run(async_body, timeout=JOB_TIMEOUT):
    """Run an async function body in the Canvas tab and return the string it resolves to.

    Arc is only busy for the instant each start, poll, or chunk read takes. The body
    must resolve to JSON or ASCII: non-ASCII is sent as \\uXXXX escapes so chunk
    boundaries never split a character."""
    key = "j" + os.urandom(6).hex()
    slot = f"window.__canvasSync[{json.dumps(key)}]"
    started = arc_eval(f"""(() => {{
        window.__canvasSync = window.__canvasSync || {{}};
        const s = {slot} = {{done: false}};
        (async () => {{ {async_body} }})().then(
            v => {{ s.value = String(v).replace(/[\\u0080-\\uffff]/g,
                c => '\\\\u' + c.charCodeAt(0).toString(16).padStart(4, '0')); s.done = true; }},
            e => {{ s.error = String(e); s.done = true; }});
        return 'started';
    }})()""")
    if started != "started":
        raise RuntimeError("Could not start a request in the Canvas tab; scan is incomplete.")
    deadline = time.monotonic() + timeout
    wait = 0.05
    try:
        while True:
            state = arc_eval(f"""(() => {{ const s = {slot};
                if (!s) return 'MISSING'; if (!s.done) return 'PENDING';
                if (s.error !== undefined) return 'ERROR:' + s.error;
                return 'LEN:' + s.value.length; }})()""")
            if state.startswith("LEN:"):
                length = int(state[4:])
                break
            if state == "MISSING":
                raise RuntimeError("The Canvas tab reloaded during the scan; scan is incomplete.")
            if state.startswith("ERROR:"):
                raise RuntimeError("Canvas request failed in Arc: " + state[6:])
            if time.monotonic() > deadline:
                raise RuntimeError("A Canvas request in Arc timed out; scan is incomplete.")
            time.sleep(wait)
            wait = min(wait * 2, POLL_SECONDS)
        chunks = []
        for start in range(0, length, CHUNK_CHARS):
            chunks.append(arc_eval(f"{slot}.value.slice({start}, {start + CHUNK_CHARS})"))
        value = "".join(chunks)
        if len(value) != length:
            raise RuntimeError("Arc returned a truncated response; scan is incomplete.")
        return value
    finally:
        try:
            arc_eval(f"(delete {slot}, 'ok')")
        except Exception:
            pass

def canvas_api_response(endpoint):
    """Read JSON and pagination headers with the existing browser session."""
    url = urljoin(CANVAS_ORIGIN, endpoint)
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != urlsplit(CANVAS_ORIGIN).netloc
            or not parsed.path.startswith("/api/v1/")):
        raise RuntimeError("Refusing a Canvas API link outside the configured Canvas origin.")
    if url in API_CACHE:
        return API_CACHE[url]
    js = f"""const r = await fetch({json.dumps(url)}, {{credentials: 'same-origin'}});
        return JSON.stringify({{status: r.status, body: await r.text(),
                               link: r.headers.get('Link') || ''}});"""
    for attempt in range(4):
        raw = browser_run(js)
        try:
            response = json.loads(raw)
            if isinstance(response, str):
                response = json.loads(response)
            status = response["status"]
        except (ValueError, TypeError, KeyError):
            raise RuntimeError("Canvas did not return a valid API response; check the signed-in Arc tab.") from None
        if status in (429, 500, 502, 503, 504) and attempt < 3:
            time.sleep(2 ** attempt)
            continue
        if status in (403, 404):
            warning = f"HTTP {status}: {parsed.path}"
            if warning not in SCAN_WARNINGS:
                print("  [UNAVAILABLE] " + warning)
                SCAN_WARNINGS.add(warning)
            return None, ""
        if status != 200:
            raise RuntimeError(f"Canvas API HTTP {status}: {parsed.path}; scan is incomplete.")
        try:
            body = json.loads(response["body"])
        except (ValueError, TypeError):
            raise RuntimeError("Canvas returned a login page or invalid JSON; scan is incomplete.") from None
        API_CACHE[url] = (body, response.get("link", ""))
        return API_CACHE[url]


def canvas_api_get(endpoint):
    return canvas_api_response(endpoint)[0]


def canvas_api_list(endpoint):
    """Follow Canvas's opaque next links, including lists shorter than per_page."""
    rows, seen = [], set()
    while endpoint:
        url = urljoin(CANVAS_ORIGIN, endpoint)
        if url in seen:
            raise RuntimeError("Canvas returned a repeated pagination link; scan is incomplete.")
        seen.add(url)
        data, link = canvas_api_response(url)
        if data is None:
            break
        if not isinstance(data, list):
            raise RuntimeError("Canvas returned an invalid list; scan is incomplete.")
        rows.extend(data)
        match = re.search(r'<([^>]+)>\s*;\s*rel="next"', link)
        endpoint = match.group(1) if match else None
    return rows

def download_file_to(url, dest_path, expected_size=None, existing_hashes=None):
    """Download a file through the Canvas tab's session; the page base64-encodes it natively."""
    print(f"  Downloading: {os.path.basename(dest_path)}...")
    dl_js = f"""const r = await fetch({json.dumps(url)}, {{credentials: 'include'}});
        if (r.status !== 200) return 'ERROR:' + r.status;
        const blob = await r.blob();
        const data = await new Promise((resolve, reject) => {{
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            reader.readAsDataURL(blob);
        }});
        return data.slice(data.indexOf(',') + 1);"""
    raw = browser_run(dl_js)
    if not isinstance(raw, str) or raw.startswith('ERROR:'):
        raise RuntimeError("Canvas file download failed: " + (raw if isinstance(raw, str) and raw.startswith("ERROR:") else "invalid response"))

    data = base64.b64decode(raw, validate=True)
    if expected_size is not None and len(data) != expected_size:
        raise RuntimeError(f"Incomplete download: expected {expected_size:,} bytes, received {len(data):,}.")
    if not dest_path.lower().endswith(('.html', '.htm')) and data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
        raise RuntimeError("Canvas returned an HTML page instead of the requested document.")
    digest = hashlib.sha256(data).hexdigest()
    if existing_hashes and digest in existing_hashes:
        print("    -> Identical content already present: " + existing_hashes[digest])
        return None
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".canvas-", dir=os.path.dirname(dest_path))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, dest_path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f"    -> Saved {len(data):,} bytes to {os.path.relpath(dest_path, REPO_ROOT)}")
    return len(data)

# ----------------------------------------------------------------------
# Local Inventory & Helpers
# ----------------------------------------------------------------------

def extract_file_ids_from_html(html_text):
    if not html_text:
        return set()
    matches = set(re.findall(r'/files/(\d+)', html_text))
    matches.update(re.findall(r'data-api-endpoint="[^"]*?/files/(\d+)"', html_text))
    matches.update(re.findall(r'/preview/(\d+)', html_text))
    matches.update(re.findall(r'attachment_id=(\d+)', html_text))
    matches.update(re.findall(r'file_id=(\d+)', html_text))
    return matches

def normalize_name(name):
    """Normalize a filename or title for comparison by stripping extensions and punctuation."""
    if not name:
        return ""
    stem = os.path.splitext(name)[0].lower()
    cleaned = re.sub(r'[^a-z0-9]+', ' ', stem)
    return " ".join(cleaned.split())

def get_local_inventory():
    inventory = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        if any(skip in root for skip in ['/.git', '/.vscode', '/.playwright-mcp']):
            continue
        for f in files:
            if f.startswith('.') or f.endswith(('.pyc', '.aux', '.log', '.out', '.toc', '.synctex.gz')):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, REPO_ROOT)
            try:
                size = os.path.getsize(full_path)
                with open(full_path, 'rb') as fp:
                    h = hashlib.sha256(fp.read()).hexdigest()
                inventory[rel_path] = {
                    "filename": f,
                    "rel_path": rel_path,
                    "full_path": full_path,
                    "size": size,
                    "sha256": h
                }
            except Exception:
                pass
    return inventory

def target_dest_for_file(course_folder, filename, source, title=None):
    """Determines appropriate directory in course folder based on filename, source, and display title."""
    if not filename or filename in (".", "..") or any(c in filename for c in ("/", "\\", "\x00")):
        raise RuntimeError("Canvas returned an invalid filename.")
    fn_lower = filename.lower()
    src_lower = source.lower()
    t_lower = (title or "").lower()
    combined = f"{fn_lower} {t_lower}"

    if course_folder == "SS1-ECON5015-ComputingMLEcon":
        if "syllabus" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        if "quiz" in combined:
            if "practice" in combined:
                return os.path.join(REPO_ROOT, course_folder, "Quizzes", "Practice", filename)
            return os.path.join(REPO_ROOT, course_folder, "Quizzes", filename)
        if "midterm" in combined or "exam" in combined:
            if "practice" in combined or "additional" in combined:
                return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Exams", "Midterm", "Practice", filename)
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Exams", "Midterm", filename)
        if "algorithmic" in combined or "efficiency" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework5", "Algorithmic_Efficiency", filename)
        if "model_selection" in combined and ("assignment" in combined or "hw" in combined):
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Model_Selection", filename)
        if "chinook" in combined or "sql" in combined or "db_2025" in combined or "northwind" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework10_DatabasesSQL", filename)
        if "world bank" in combined or "api" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework9_WorldBankAPI", filename)
        if "datawrangling" in combined or "data_wrangling" in combined or "wrangling" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework8_DataWrangling", filename)
        m_hw = re.search(r'(?:hw|homework)\s*(\d+)', combined)
        if m_hw:
            hw_num = m_hw.group(1)
            hw_folder = f"Homework{hw_num}"
            if os.path.isdir(os.path.join(REPO_ROOT, course_folder, "Homeworks", hw_folder)):
                return os.path.join(REPO_ROOT, course_folder, "Homeworks", hw_folder, filename)
        if fn_lower.endswith(('.ipynb', '.html')):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        if fn_lower.endswith('.py'):
            return os.path.join(REPO_ROOT, course_folder, "Scripts", filename)
        if fn_lower.endswith(('.pptx', '.pdf')) or "statistical learning" in combined or "model_selection" in combined or "database" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
        if fn_lower.endswith('.csv'):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        if "hw" in combined or "assignment" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", filename)
        return os.path.join(REPO_ROOT, course_folder, "Resources", filename)

    elif course_folder == "SS1-ECON5560-AppliedEconProj1":
        if "presentation" in src_lower or "presentation" in combined or "slidedoc" in combined or "zettlemeyer" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Deliverables", "Presentation", "Resources", filename)
        if "replication" in combined or "charter" in combined or "milestone" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Replication-Project", "Resources", filename)
        return os.path.join(REPO_ROOT, course_folder, "Resources", filename)

    elif course_folder == "SS1-ECON5021-AdvEconometrics1":
        if "proposal" in combined or "replication" in combined or "replication" in src_lower:
            return os.path.join(REPO_ROOT, course_folder, "Replication_Project", filename)
        if "exam 1" in combined or "exam1" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Exam1", filename)
        if "exam 2" in combined or "exam2" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Exam2", filename)
        if fn_lower.endswith('.pdf') and ("lecture" in combined or "note" in combined):
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
        if "practice" in combined or "in_class" in combined:
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Practice", filename)
        if "syllabus" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        return os.path.join(REPO_ROOT, course_folder, "Exercises", filename)

    elif course_folder == "SS1-ECON5030-MicroeconomicAnalysis":
        if "syllabus" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        if "midterm" in combined or "exam" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Midterm", filename)
        if "problem set" in combined or "ps" in combined or "ak" in combined:
            m = re.search(r'set\s*(\d+)', combined)
            ps_num = m.group(1) if m else "1"
            return os.path.join(REPO_ROOT, course_folder, "ProblemSets", f"ProblemSet{ps_num}", filename)
        return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)

    elif course_folder == "SS1-ECON5040-DynamicStochasticModeling":
        if "prelim" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", "Exams", "Prelim", filename)
        if "midterm" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", "Exams", "Midterm", filename)
        if re.search(r'\bweek[ _-]*11(?=\D|$)', combined):
            if "problem_set" in combined or "starter" in combined:
                return os.path.join(REPO_ROOT, course_folder, "ProblemSets", "ProblemSet10", filename)
            if fn_lower.endswith('.ipynb'):
                return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", "Week11_Asset_Pricing", filename)
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week11_Lucas_Tree", filename)
        if "week12" in combined or "complete_markets" in combined or "arrow_securities" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week12_Complete_Markets", filename)
        if re.search(r'\bweek[ _-]*1(?=\D|$)', combined) or "intertemporal" in combined or "slutsky" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week1_Intertemporal_Choice", filename)
        if "final" in src_lower or "final" in combined:
            if "project" in combined or "sir" in combined or fn_lower.endswith('.ipynb'):
                return os.path.join(REPO_ROOT, course_folder, "Final_Project", filename)
            if fn_lower.endswith(('.pdf', '.doc', '.docx')):
                return os.path.join(REPO_ROOT, course_folder, "Readings", filename)
            return os.path.join(REPO_ROOT, course_folder, "Final_Project", filename)
        m_ps = re.search(r'(?:problem_set_|ps)(\d+)', combined)
        if m_ps:
            return os.path.join(REPO_ROOT, course_folder, "ProblemSets", f"ProblemSet{m_ps.group(1)}", filename)
        if fn_lower.endswith('.ipynb'):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        return os.path.join(REPO_ROOT, course_folder, "Readings", filename)

    elif course_folder == "SP26-ECON470-MicroeconAI":
        if "syllabus" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        if "lab" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Labs", filename)
        if "exam" in combined or "midterm" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Exams", filename)
        if "pres" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Presentations", filename)
        if "reading" in combined or "essay" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Readings", filename)
        if "lecture" in combined or fn_lower.endswith(('.pptx', '.pdf')):
            return os.path.join(REPO_ROOT, course_folder, "Lectures", filename)
        return os.path.join(REPO_ROOT, course_folder, "Readings", filename)

    elif course_folder == "SU26-GSE510-MathEcon":
        if "syllabus" in combined:
            return os.path.join(REPO_ROOT, course_folder, filename)
        if "homework" in combined or "hw" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", filename)
        if "practice" in combined and "exam" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Practice Exams", filename)
        if "exam" in combined and ("solution" in combined or "sol" in combined):
            return os.path.join(REPO_ROOT, course_folder, "Exam Solutions", filename)
        if "claude" in combined:
            return os.path.join(REPO_ROOT, course_folder, "Claude Exams", filename)
        if "lecture" in combined or fn_lower.endswith(('.pdf', '.pptx')):
            return os.path.join(REPO_ROOT, course_folder, "Lecture Notes", filename)
        return os.path.join(REPO_ROOT, course_folder, "Homeworks", filename)

    elif course_folder == "EXT/Graduate_Student_Materials":
        return os.path.join(REPO_ROOT, course_folder, filename)

    return os.path.join(REPO_ROOT, course_folder, "Resources", filename)

# ----------------------------------------------------------------------
# Core Routine
# ----------------------------------------------------------------------

def run_sync(dry_run=False, push=False):
    API_CACHE.clear()
    SCAN_WARNINGS.clear()
    print("=" * 60)
    if push:
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
        if staged.returncode:
            raise RuntimeError("Existing staged changes must be committed separately before using --push.")
    print("MSQE Canvas Routine: Starting course differential sync")
    print("=" * 60)

    # 1. Verify Canvas tab in Arc
    tab_status = find_canvas_tab()
    if not tab_status or "NOT_FOUND" in tab_status:
        print("[ERROR] Canvas tab is not currently open or logged in within Arc.")
        print("Please ensure https://canvas.calpoly.edu is loaded in an Arc tab.")
        sys.exit(1)

    user = canvas_api_get('/api/v1/users/self')
    if not user or not user.get('id'):
        print("[ERROR] Canvas tab is not currently open or logged in within Arc.")
        print("Please ensure https://canvas.calpoly.edu is loaded in an Arc tab.")
        sys.exit(1)
    print(f"Authenticated as: {user.get('name')} (ID: {user.get('id')})")

    # 2. Index local repository
    local_inv = get_local_inventory()
    protected = set()
    for flags in (("-m", "-d"), ("--others", "--exclude-standard")):
        result = subprocess.run(["git", "ls-files", "-z", *flags], cwd=REPO_ROOT, capture_output=True, check=True)
        protected.update(os.path.join(REPO_ROOT, os.fsdecode(path)) for path in result.stdout.split(b"\0") if path)
    # Staged changes also belong to their existing writer.
    result = subprocess.run(["git", "diff", "--cached", "--name-only", "-z"], cwd=REPO_ROOT, capture_output=True, check=True)
    protected.update(os.path.join(REPO_ROOT, os.fsdecode(path)) for path in result.stdout.split(b"\0") if path)
    print(f"Indexed {len(local_inv)} local files in MSQE_Stuff.")

    local_by_folder = {}
    for rel_path, finfo in local_inv.items():
        matched_fld = None
        for fld in COURSE_MAP.values():
            if rel_path.startswith(fld + os.sep) or rel_path == fld:
                matched_fld = fld
                break
        if not matched_fld:
            matched_fld = rel_path.split(os.sep)[0]
        local_by_folder.setdefault(matched_fld, []).append(finfo)

    # 3. Scan each course comprehensively
    differentials = [] # list of (url, dest_path, file_meta, folder, is_update)
    planned = set()
    
    for cid, folder in COURSE_MAP.items():
        print(f"\nScanning {folder} (ID: {cid})...")
        course_files = {}

        # 3a. Direct files endpoint (handles pagination)
        for f in canvas_api_list(f'/api/v1/courses/{cid}/files?per_page=100'):
            if f.get('id'):
                course_files[str(f['id'])] = {"source": "files_api", "title": f.get('display_name'), "meta": f}

        # 3b. Modules and module items
        modules = canvas_api_list(f'/api/v1/courses/{cid}/modules?include[]=items&per_page=100')
        if isinstance(modules, list):
            for m in modules:
                m_name = m.get('name', '')
                items = m.get('items')
                if not isinstance(items, list) or len(items) < m.get('items_count', 0):
                    items = canvas_api_list(f'/api/v1/courses/{cid}/modules/{m["id"]}/items?per_page=100')
                for item in items:
                    itype = item.get('type')
                    fid = item.get('content_id')
                    title = item.get('title')
                    if itype == 'File' and fid and str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"module:{m_name}", "title": title, "meta": None}
                    elif itype == 'Page' and item.get('page_url'):
                        p = canvas_api_get(f'/api/v1/courses/{cid}/pages/{item.get("page_url")}')
                        if isinstance(p, dict):
                            for pfid in extract_file_ids_from_html(p.get('body', '')):
                                if str(pfid) not in course_files:
                                    course_files[str(pfid)] = {"source": f"module_page:{m_name}/{title}", "title": None, "meta": None}
                    elif itype == 'Assignment' and item.get('url'):
                        a_data = canvas_api_get(item.get('url'))
                        if isinstance(a_data, dict):
                            for afid in extract_file_ids_from_html(a_data.get('description', '')):
                                if str(afid) not in course_files:
                                    course_files[str(afid)] = {"source": f"module_assignment:{m_name}/{title}", "title": None, "meta": None}

        # 3c. All published Course Pages (including those not placed in modules)
        all_pages = canvas_api_list(f'/api/v1/courses/{cid}/pages?per_page=100')
        if isinstance(all_pages, list):
            for p_meta in all_pages:
                p_url = p_meta.get('url')
                p_title = p_meta.get('title')
                if p_url:
                    p = canvas_api_get(f'/api/v1/courses/{cid}/pages/{p_url}')
                    if isinstance(p, dict):
                        for pfid in extract_file_ids_from_html(p.get('body', '')):
                            if str(pfid) not in course_files:
                                course_files[str(pfid)] = {"source": f"page:{p_title}", "title": None, "meta": None}

        # 3d. Assignments (description & attachments)
        assignments = canvas_api_list(f'/api/v1/courses/{cid}/assignments?per_page=100')
        if isinstance(assignments, list):
            for a in assignments:
                a_name = a.get('name', '')
                for fid in extract_file_ids_from_html(a.get('description', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"assignment:{a_name}", "title": None, "meta": None}
                for att in a.get('attachments', []):
                    fid = str(att.get('id'))
                    if fid and fid not in course_files:
                        course_files[fid] = {"source": f"assignment_att:{a_name}", "title": att.get('display_name'), "meta": att}

        # 3e. Announcements
        announcements = canvas_api_list(f'/api/v1/courses/{cid}/discussion_topics?only_announcements=true&per_page=50')
        if isinstance(announcements, list):
            for ann in announcements:
                ann_title = ann.get('title', '')
                for fid in extract_file_ids_from_html(ann.get('message', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"announcement:{ann_title}", "title": None, "meta": None}
                for att in ann.get('attachments', []):
                    fid = str(att.get('id'))
                    if fid and fid not in course_files:
                        course_files[fid] = {"source": f"announcement_att:{ann_title}", "title": att.get('display_name'), "meta": att}

        # 3f. Discussions (non-announcements)
        discussions = canvas_api_list(f'/api/v1/courses/{cid}/discussion_topics?per_page=50')
        if isinstance(discussions, list):
            for disc in discussions:
                disc_title = disc.get('title', '')
                for fid in extract_file_ids_from_html(disc.get('message', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"discussion:{disc_title}", "title": None, "meta": None}
                for att in disc.get('attachments', []):
                    fid = str(att.get('id'))
                    if fid and fid not in course_files:
                        course_files[fid] = {"source": f"discussion_att:{disc_title}", "title": att.get('display_name'), "meta": att}

        # 3g. Syllabus
        c_info = canvas_api_get(f'/api/v1/courses/{cid}?include[]=syllabus_body')
        if isinstance(c_info, dict) and c_info.get('syllabus_body'):
            for fid in extract_file_ids_from_html(c_info.get('syllabus_body')):
                if str(fid) not in course_files:
                    course_files[str(fid)] = {"source": "syllabus", "title": None, "meta": None}

        # 3h. Quizzes (description)
        quizzes = canvas_api_list(f'/api/v1/courses/{cid}/quizzes?per_page=100')
        if isinstance(quizzes, list):
            for q in quizzes:
                q_title = q.get('title', '')
                for fid in extract_file_ids_from_html(q.get('description', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"quiz:{q_title}", "title": None, "meta": None}

        # 3i. Batch resolve ALL unresolved metadata in browser context
        unresolved_fids = [fid for fid, finfo in course_files.items() if not finfo.get("meta")]
        if unresolved_fids:
            chunk_size = 30
            for i in range(0, len(unresolved_fids), chunk_size):
                chunk = unresolved_fids[i:i+chunk_size]
                batch_js = f"""const fids = {json.dumps(chunk)};
                    const out = {{}};
                    let next = 0;
                    const worker = async () => {{
                        while (next < fids.length) {{
                            const id = fids[next++];
                            const r = await fetch('/api/v1/files/' + id, {{credentials: 'same-origin'}});
                            if (r.status === 200) {{
                                try {{ out[id] = JSON.parse(await r.text()); }} catch(e) {{}}
                            }} else {{
                                out[id] = {{_http_status: r.status}};
                            }}
                        }}
                    }};
                    await Promise.all(Array.from({{length: 4}}, worker));
                    return JSON.stringify(out);"""
                raw_res = browser_run(batch_js)
                try:
                    if isinstance(raw_res, str):
                        batch_data = json.loads(raw_res)
                        if isinstance(batch_data, str):
                            batch_data = json.loads(batch_data)
                    else:
                        batch_data = raw_res
                    if isinstance(batch_data, dict):
                        for id_str, m in batch_data.items():
                            if id_str in course_files:
                                if "_http_status" in m:
                                    status = m["_http_status"]
                                    if status not in (403, 404):
                                        raise RuntimeError(f"Canvas file metadata HTTP {status}; scan is incomplete.")
                                    warning = f"HTTP {status}: /api/v1/files/{id_str}"
                                    SCAN_WARNINGS.add(warning)
                                    print("  [UNAVAILABLE] " + warning)
                                    continue
                                course_files[id_str]["meta"] = m
                except (ValueError, TypeError):
                    raise RuntimeError("Canvas file metadata response was invalid; scan is incomplete.") from None

        # 3j. Differentiate against local files
        local_files = local_by_folder.get(folder, [])
        local_filenames_lower = {item["filename"].lower(): item for item in local_files}
        local_norm_to_file = {}
        for item in local_files:
            norm = normalize_name(item["filename"])
            item_ext = os.path.splitext(item["filename"])[1].lower()
            if norm:
                local_norm_to_file[(norm, item_ext)] = item

        for fid, finfo in course_files.items():
            meta = finfo.get("meta")
            title = finfo.get("title")
            filename = (meta.get("display_name") or meta.get("filename")) if meta else title
            if not filename:
                continue
            canvas_size = meta.get("size") if meta else None
            canvas_url = meta.get("url") if meta else None
            ext = os.path.splitext(filename)[1].lower()

            # Skip small non-document announcement icons
            if filename.lower() in ['image.png', 'images.jpeg'] and canvas_size and canvas_size < 500000 and "announcement" in finfo["source"].lower():
                continue

            matched_local = local_filenames_lower.get(filename.lower())

            # 1. Match by module item display title + file extension
            if not matched_local and title:
                title_clean = title.strip()
                title_ext = f"{title_clean}{ext}".lower()
                matched_local = local_filenames_lower.get(title_ext)

            # 2. Match by normalized filename with same extension
            if not matched_local:
                norm_fn = normalize_name(filename)
                matched_local = local_norm_to_file.get((norm_fn, ext))

            # 3. Match by normalized title with same extension
            if not matched_local and title:
                norm_title = normalize_name(title)
                matched_local = local_norm_to_file.get((norm_title, ext))

            if matched_local:
                # If notebook or code was executed locally, size differences are normal — skip overwriting
                if filename.lower().endswith(('.ipynb', '.py')) or (canvas_size and matched_local["size"] == canvas_size) or canvas_size is None:
                    continue
                # If size differs on a document file (e.g. updated lecture slides, study guide, syllabus), update it in place!
                if canvas_size and matched_local["size"] != canvas_size:
                    if canvas_url:
                        dest = matched_local["full_path"]
                        if dest in protected:
                            stem, ext = os.path.splitext(dest)
                            dest = f"{stem} (Canvas {fid}){ext}"
                        if dest not in protected and dest not in planned:
                            differentials.append((canvas_url, dest, meta, folder, dest == matched_local["full_path"]))
                            planned.add(dest)
                        else:
                            print(f"  [PRESERVED] Local changes: {os.path.relpath(dest, REPO_ROOT)}")
                    continue

            if not canvas_url:
                continue

            dest_path = target_dest_for_file(folder, filename, finfo["source"], title=title)
            if dest_path in protected or dest_path in planned:
                stem, ext = os.path.splitext(dest_path)
                dest_path = f"{stem} (Canvas {fid}){ext}"
            if dest_path in protected or dest_path in planned:
                raise RuntimeError("A Canvas destination conflicts with existing local work.")
            differentials.append((canvas_url, dest_path, meta, folder, False))
            planned.add(dest_path)
        print(f"  Found {len(course_files)} referenced files.")

    # 4. Check Downloads folder for recent course materials
    downloads_proposal = os.path.join(DOWNLOADS_DIR, "Replication Project Part 1 Proposal, Due 1028.pdf")
    dest_proposal = os.path.join(REPO_ROOT, "SS1-ECON5021-AdvEconometrics1/Replication_Project/Replication Project Part 1 Proposal, Due 1028.pdf")
    if os.path.exists(downloads_proposal) and not os.path.exists(dest_proposal):
        differentials.append(("file://" + downloads_proposal, dest_proposal, {"display_name": os.path.basename(downloads_proposal)}, "SS1-ECON5021-AdvEconometrics1", False))

    print("\n" + "=" * 60)
    print(f"DIFFERENTIALS FOUND: {len(differentials)} course file(s)")
    if SCAN_WARNINGS:
        print(f"Canvas restricted {len(SCAN_WARNINGS)} API endpoint(s); accessible sources were scanned.")
    print("=" * 60)
    for url, dest, meta, fld, is_update in differentials:
        tag = "[UPDATE]" if is_update else "[NEW]"
        csize = meta.get("size") if meta else 0
        size_str = f" ({csize:,} bytes)" if csize else ""
        print(f"  {tag} [{fld}] {os.path.basename(dest)}{size_str} -> {os.path.relpath(dest, REPO_ROOT)}")

    if dry_run or not differentials:
        if dry_run:
            print("\nDry-run mode: no files downloaded or committed.")
        else:
            print("\nNo new downloadable materials found in the accessible Canvas sources.")
        return []

    # 5. Download differentials
    created_paths = []
    failures = []
    print("\nDownloading course materials...")
    for url, dest, meta, fld, is_update in differentials:
        try:
            if url.startswith("file://"):
                src_path = url[7:]
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src_path, dest)
                print(f"  Organized: {os.path.basename(dest)} -> {os.path.relpath(dest, REPO_ROOT)}")
            else:
                hashes = {item["sha256"]: item["rel_path"] for item in local_by_folder.get(fld, [])}
                if download_file_to(url, dest, expected_size=meta.get("size"), existing_hashes=hashes) is None:
                    continue
            created_paths.append(os.path.relpath(dest, REPO_ROOT))
            local_by_folder.setdefault(fld, []).append({
                "sha256": hashlib.sha256(Path(dest).read_bytes()).hexdigest(),
                "rel_path": os.path.relpath(dest, REPO_ROOT)})
        except Exception as e:
            print(f"  [ERROR] Failed to save {os.path.basename(dest)}: {e}")
            failures.append(os.path.basename(dest))

    report = {"created_paths": created_paths, "failed_files": failures,
              "restricted_endpoints": sorted(SCAN_WARNINGS), "dry_run": False}
    report_path = os.environ.get("CANVAS_SYNC_REPORT")
    if report_path:
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
    print(f"\nSaved {len(created_paths)} files; {len(failures)} downloads failed.")
    if failures:
        raise RuntimeError("Canvas sync is incomplete; failed downloads are listed above. No commit was made.")

    # 6. Commit & Push if requested
    if push and created_paths:
        print("\n" + "=" * 60)
        print("Committing and pushing following AGENTS.md rules...")
        print("=" * 60)
        # Stage only this invocation's downloads, never unrelated script edits.
        paths_to_stage = list(created_paths)
        if any(os.path.getsize(os.path.join(REPO_ROOT, path)) > 50 * 1024 * 1024 for path in paths_to_stage):
            raise RuntimeError("A download exceeds the repository's 50 MB commit limit; files remain local.")
        subprocess.run(["git", "add", "--"] + paths_to_stage, cwd=REPO_ROOT, check=True)
        # Commit once per prompt
        msg = "Canvas sync: update course materials and improve sync routine"
        subprocess.run(["git", "commit", "-m", msg], cwd=REPO_ROOT, check=True)
        # Rebase sync
        subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"], cwd=REPO_ROOT, check=True)
        # Verify only self commit is being pushed
        log_p = subprocess.run(["git", "log", "--format=%h %s", "origin/main..HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        lines = [line.strip() for line in log_p.stdout.strip().splitlines() if line.strip()]
        if len(lines) != 1:
            print(f"[GUARD] Multiple or unexpected unpushed commits detected ({len(lines)}). Aborting push.")
            print(log_p.stdout)
            return
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, check=True)
        rev_p = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        print(f"Committed {rev_p.stdout.strip()} and pushed.")
    return created_paths

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sync Canvas course differentials to MSQE_Stuff")
    parser.add_argument("--dry-run", action="store_true", help="Scan and list differences without downloading")
    parser.add_argument("--push", action="store_true", help="Automatically commit and push added materials according to AGENTS.md")
    args = parser.parse_args()
    try:
        run_sync(dry_run=args.dry_run, push=args.push)
    except (RuntimeError, subprocess.SubprocessError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
