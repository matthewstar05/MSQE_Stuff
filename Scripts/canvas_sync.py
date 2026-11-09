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

def find_canvas_tab():
    """Checks if an authenticated Canvas tab is open in Arc without focusing or selecting if already active."""
    applescript = '''
    tell application "Arc"
        try
            if (URL of active tab of front window) starts with "https://canvas.calpoly.edu" then
                return (URL of active tab of front window)
            end if
        end try
        repeat with w in windows
            try
                if (URL of active tab of w) starts with "https://canvas.calpoly.edu" then
                    return (URL of active tab of w)
                end if
            end try
        end repeat
        repeat with w in windows
            repeat with t in tabs of w
                try
                    if (URL of t) starts with "https://canvas.calpoly.edu" then
                        return (URL of t)
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
    return p.stdout.strip()

def arc_eval(js_code):
    """Executes JavaScript inside an authenticated Canvas tab in Arc."""
    escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    applescript = f'''
    tell application "Arc"
        try
            if (URL of active tab of front window) starts with "https://canvas.calpoly.edu" then
                return (execute active tab of front window javascript "{escaped_js}")
            end if
        end try
        repeat with w in windows
            try
                if (URL of active tab of w) starts with "https://canvas.calpoly.edu" then
                    return (execute active tab of w javascript "{escaped_js}")
                end if
            end try
        end repeat
        repeat with w in windows
            repeat with t in tabs of w
                try
                    if (URL of t) starts with "https://canvas.calpoly.edu" then
                        select t
                        delay 0.2
                        return (execute t javascript "{escaped_js}")
                    end if
                end try
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    p = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, timeout=90)
    if p.returncode != 0:
        raise RuntimeError(f"AppleScript error: {p.stderr.strip()}")
    res = p.stdout.strip()
    if res.startswith('"') and res.endswith('"'):
        try:
            res = json.loads(res)
        except Exception:
            pass
    return res

def canvas_api_response(endpoint):
    """Read JSON and pagination headers with the existing browser session."""
    url = urljoin(CANVAS_ORIGIN, endpoint)
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != urlsplit(CANVAS_ORIGIN).netloc
            or not parsed.path.startswith("/api/v1/")):
        raise RuntimeError("Refusing a Canvas API link outside the configured Canvas origin.")
    if url in API_CACHE:
        return API_CACHE[url]
    js = f"""(() => {{
        const xhr = new XMLHttpRequest();
        xhr.open('GET', {json.dumps(url)}, false);
        xhr.send(null);
        return JSON.stringify({{status: xhr.status, body: xhr.responseText,
                               link: xhr.getResponseHeader('Link') || ''}});
    }})()"""
    for attempt in range(4):
        raw = arc_eval(js)
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
    """Downloads a file in a single synchronous background call using fast base64 encoding."""
    print(f"  Downloading: {os.path.basename(dest_path)}...")
    dl_js = f"""(() => {{
        const xhr = new XMLHttpRequest();
        xhr.open('GET', {json.dumps(url)}, false);
        xhr.overrideMimeType('text/plain; charset=x-user-defined');
        xhr.send(null);
        if (xhr.status !== 200) return 'ERROR:' + xhr.status;
        const bin = xhr.responseText;
        const len = bin.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) bytes[i] = bin.charCodeAt(i) & 0xff;
        
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        let out = '';
        const extra = len % 3;
        const main = len - extra;
        for (let i = 0; i < main; i += 3) {{
            const b0 = bytes[i], b1 = bytes[i+1], b2 = bytes[i+2];
            out += chars[b0 >> 2] + chars[((b0 & 3) << 4) | (b1 >> 4)] + chars[((b1 & 15) << 2) | (b2 >> 6)] + chars[b2 & 63];
        }}
        if (extra === 1) {{
            const b0 = bytes[main];
            out += chars[b0 >> 2] + chars[(b0 & 3) << 4] + '==';
        }} else if (extra === 2) {{
            const b0 = bytes[main], b1 = bytes[main+1];
            out += chars[b0 >> 2] + chars[((b0 & 3) << 4) | (b1 >> 4)] + chars[(b1 & 15) << 2] + '=';
        }}
        return out;
    }})()"""
    raw = arc_eval(dl_js)
    if isinstance(raw, str) and raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    if not isinstance(raw, str) or raw.startswith('ERROR:') or raw == 'NOT_FOUND':
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
    return matches

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

def target_dest_for_file(course_folder, filename, source):
    """Determines appropriate directory in course folder based on filename & source."""
    if not filename or filename in (".", "..") or any(c in filename for c in ("/", "\\", "\x00")):
        raise RuntimeError("Canvas returned an invalid filename.")
    fn_lower = filename.lower()
    src_lower = source.lower()

    if course_folder == "SS1-ECON5015-ComputingMLEcon":
        if "syllabus" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        if "model_selection" in fn_lower and ("assignment" in fn_lower or "hw" in fn_lower):
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Model_Selection", filename)
        if "chinook" in fn_lower or "sql" in fn_lower or "db_2025" in fn_lower or "northwind" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework10_DatabasesSQL", filename)
        if fn_lower.endswith(('.ipynb', '.html')):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        if fn_lower.endswith('.py'):
            return os.path.join(REPO_ROOT, course_folder, "Scripts", filename)
        if "world bank" in fn_lower or "api" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework9_WorldBankAPI", filename)
        if fn_lower.endswith(('.pptx', '.pdf')) or "statistical learning" in fn_lower or "model_selection" in fn_lower or "database" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
        if fn_lower.endswith('.csv'):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        if "hw" in fn_lower or "assignment" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", filename)
        return os.path.join(REPO_ROOT, course_folder, "Resources", filename)

    elif course_folder == "SS1-ECON5560-AppliedEconProj1":
        if "presentation" in src_lower or "slidedoc" in fn_lower or "zettlemeyer" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Deliverables", "Presentation", "Resources", filename)
        return os.path.join(REPO_ROOT, course_folder, "Resources", filename)

    elif course_folder == "SS1-ECON5021-AdvEconometrics1":
        if "proposal" in fn_lower or "replication" in fn_lower or "replication" in src_lower:
            return os.path.join(REPO_ROOT, course_folder, "Replication_Project", filename)
        if fn_lower.endswith('.pdf') and ("lecture" in fn_lower or "note" in fn_lower):
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
        if "syllabus" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", filename)
        return os.path.join(REPO_ROOT, course_folder, "Exercises", filename)

    elif course_folder == "SS1-ECON5030-MicroeconomicAnalysis":
        if "problem set" in fn_lower or "ps" in fn_lower or "ak" in fn_lower:
            m = re.search(r'set\s*(\d+)', fn_lower)
            ps_num = m.group(1) if m else "1"
            return os.path.join(REPO_ROOT, course_folder, "ProblemSets", f"ProblemSet{ps_num}", filename)
        return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)

    elif course_folder == "SS1-ECON5040-DynamicStochasticModeling":
        if "prelim" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Exams", "Prelim", filename)
        if "final" in src_lower or "final" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Exams", "Final", filename)
        if "midterm" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Course_Info", "Exams", "Midterm", filename)
        if re.search(r'\bweek[ _-]*11(?=\D|$)', fn_lower):
            if "problem_set" in fn_lower or "starter" in fn_lower:
                return os.path.join(REPO_ROOT, course_folder, "ProblemSets", "ProblemSet10", filename)
            if fn_lower.endswith('.ipynb'):
                return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", "Week11_Asset_Pricing", filename)
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week11_Lucas_Tree", filename)
        if "week12" in fn_lower or "complete_markets" in fn_lower or "arrow_securities" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week12_Complete_Markets", filename)
        if re.search(r'\bweek[ _-]*1(?=\D|$)', fn_lower) or "intertemporal" in fn_lower or "slutsky" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week1_Intertemporal_Choice", filename)
        m_ps = re.search(r'(?:problem_set_|ps)(\d+)', fn_lower)
        if m_ps:
            return os.path.join(REPO_ROOT, course_folder, "ProblemSets", f"ProblemSet{m_ps.group(1)}", filename)
        if fn_lower.endswith('.ipynb'):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        return os.path.join(REPO_ROOT, course_folder, "Readings", filename)

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

        # 3h. Batch resolve ALL unresolved metadata in browser context
        unresolved_fids = [fid for fid, finfo in course_files.items() if not finfo.get("meta")]
        if unresolved_fids:
            chunk_size = 30
            for i in range(0, len(unresolved_fids), chunk_size):
                chunk = unresolved_fids[i:i+chunk_size]
                batch_js = f"""(() => {{
                    const fids = {json.dumps(chunk)};
                    const out = {{}};
                    for (const id of fids) {{
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', '/api/v1/files/' + id, false);
                        xhr.send(null);
                        if (xhr.status === 200) {{
                            try {{ out[id] = JSON.parse(xhr.responseText); }} catch(e) {{}}
                        }} else {{
                            out[id] = {{_http_status: xhr.status}};
                        }}
                    }}
                    return JSON.stringify(out);
                }})()"""
                raw_res = arc_eval(batch_js)
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

        # 3i. Differentiate against local files
        local_files = local_by_folder.get(folder, [])
        local_filenames_lower = {item["filename"].lower(): item for item in local_files}

        for fid, finfo in course_files.items():
            meta = finfo.get("meta")
            title = finfo.get("title")
            filename = (meta.get("display_name") or meta.get("filename")) if meta else title
            if not filename:
                continue
            canvas_size = meta.get("size") if meta else None
            canvas_url = meta.get("url") if meta else None

            # Skip small non-document announcement icons
            if filename.lower() in ['image.png', 'images.jpeg'] and canvas_size and canvas_size < 500000 and "announcement" in finfo["source"].lower():
                continue

            # Equal byte sizes across different names do not establish identity.
            matched_local = local_filenames_lower.get(filename.lower())

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

            dest_path = target_dest_for_file(folder, filename, finfo["source"])
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
