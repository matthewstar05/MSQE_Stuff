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

REPO_ROOT = "/Users/star/Desktop/Academic/MSQE_Stuff"
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

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
    """Checks if an authenticated Canvas tab is open in Arc without focusing or selecting it."""
    applescript = '''
    tell application "Arc"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) starts with "https://canvas.calpoly.edu" then
                    return URL of t
                end if
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    p = subprocess.run(['osascript'], input=applescript, capture_output=True, text=True)
    return p.stdout.strip()

def arc_eval(js_code):
    """Executes JavaScript inside the Canvas tab in Arc completely in the background without focusing or selecting."""
    applescript = f'''
    tell application "Arc"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t) starts with "https://canvas.calpoly.edu" then
                    return (execute t javascript "{js_code}")
                end if
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    p = subprocess.run(['osascript'], input=applescript, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"AppleScript error: {p.stderr.strip()}")
    return p.stdout.strip()

def canvas_api_get(endpoint):
    """Calls Canvas API synchronously using XMLHttpRequest within the browser context."""
    js = f"""(() => {{
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '{endpoint}', false);
        xhr.send(null);
        return xhr.responseText;
    }})()"""
    escaped_js = js.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    raw = arc_eval(escaped_js)
    try:
        parsed_str = json.loads(raw)
        if isinstance(parsed_str, str):
            parsed_str = json.loads(parsed_str)
        return parsed_str
    except Exception:
        return None

def download_file_to(url, dest_path):
    """Downloads a file in a single synchronous background call without polling or tab selection."""
    print(f"  Downloading: {os.path.basename(dest_path)}...")
    dl_js = f"""(() => {{
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '{url}', false);
        xhr.overrideMimeType('text/plain; charset=x-user-defined');
        xhr.send(null);
        if (xhr.status !== 200) return 'ERROR:' + xhr.status;
        const bin = xhr.responseText;
        let binary = '';
        for (let i = 0; i < bin.length; i++) {{
            binary += String.fromCharCode(bin.charCodeAt(i) & 0xff);
        }}
        return btoa(binary);
    }})()"""
    escaped_dl_js = dl_js.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    raw = arc_eval(escaped_dl_js)
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    if raw.startswith('ERROR:') or raw == 'NOT_FOUND':
        raise RuntimeError(f"Download failed for {url}: {raw}")

    data = base64.b64decode(raw)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
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
    fn_lower = filename.lower()
    src_lower = source.lower()

    if course_folder == "SS1-ECON5015-ComputingMLEcon":
        if "chinook" in fn_lower or "sql" in fn_lower or "db_2025" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework10_DatabasesSQL", filename)
        if fn_lower.endswith('.ipynb') or fn_lower.endswith('.html'):
            return os.path.join(REPO_ROOT, course_folder, "In_Class_Notebooks", filename)
        if "world bank" in fn_lower or "api" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Homeworks", "Homework9_WorldBankAPI", filename)
        if fn_lower.endswith('.pptx') or "database" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
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
        if fn_lower.endswith('.pdf') and "lecture" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", filename)
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
        if "midterm" in fn_lower and "key" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Exams", "Midterm", filename)
        if "week12_problem_set" in fn_lower or "ps11" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "ProblemSets", "ProblemSet11", filename)
        if "complete_markets" in fn_lower or "arrow_securities" in fn_lower or "week12" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week12_Complete_Markets", filename)
        if "income_substitution" in fn_lower:
            return os.path.join(REPO_ROOT, course_folder, "Lecture_Notes", "Week1_Intertemporal_Choice", filename)
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
    print("=" * 60)
    print("MSQE Canvas Routine: Starting course differential sync")
    print("=" * 60)

    # 1. Verify Canvas tab in Arc (completely in background, never select/focus)
    tab_status = find_canvas_tab()
    if "NOT_FOUND" in tab_status:
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

    # 3. Scan each course
    differentials = [] # list of (url, dest_path, file_meta, folder)
    
    for cid, folder in COURSE_MAP.items():
        print(f"\nScanning {folder} (ID: {cid})...")
        course_files = {}

        # Direct files check
        files_list = canvas_api_get(f'/api/v1/courses/{cid}/files?per_page=100')
        if isinstance(files_list, list):
            for f in files_list:
                fid = f.get('id')
                if fid:
                    course_files[str(fid)] = {"source": "files_api", "title": f.get('display_name'), "meta": f}

        # Modules
        modules = canvas_api_get(f'/api/v1/courses/{cid}/modules?include[]=items&per_page=100')
        if isinstance(modules, list):
            for m in modules:
                m_name = m.get('name', '')
                for item in m.get('items', []):
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
                                    course_files[str(pfid)] = {"source": f"page:{m_name}/{title}", "title": None, "meta": None}

        # Assignments
        assignments = canvas_api_get(f'/api/v1/courses/{cid}/assignments?per_page=100')
        if isinstance(assignments, list):
            for a in assignments:
                for fid in extract_file_ids_from_html(a.get('description', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"assignment:{a.get('name')}", "title": None, "meta": None}

        # Announcements
        announcements = canvas_api_get(f'/api/v1/courses/{cid}/discussion_topics?only_announcements=true&per_page=50')
        if isinstance(announcements, list):
            for ann in announcements:
                for fid in extract_file_ids_from_html(ann.get('message', '')):
                    if str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"announcement:{ann.get('title')}", "title": None, "meta": None}
                for att in ann.get('attachments', []):
                    fid = att.get('id')
                    if fid and str(fid) not in course_files:
                        course_files[str(fid)] = {"source": f"announcement:{ann.get('title')}", "title": att.get('display_name'), "meta": att}

        # Syllabus
        c_info = canvas_api_get(f'/api/v1/courses/{cid}?include[]=syllabus_body')
        if isinstance(c_info, dict) and c_info.get('syllabus_body'):
            for fid in extract_file_ids_from_html(c_info.get('syllabus_body')):
                if str(fid) not in course_files:
                    course_files[str(fid)] = {"source": "syllabus", "title": None, "meta": None}

        # Resolve metadata efficiently
        local_files = local_by_folder.get(folder, [])
        local_filenames_lower = {item["filename"].lower(): item for item in local_files}
        local_sizes = {item["size"]: item for item in local_files}

        # Fast-path: only resolve files that do not directly match an existing local filename
        unresolved_fids = []
        for fid, finfo in course_files.items():
            if finfo.get("meta"):
                continue
            title = finfo.get("title")
            if title and title.lower() in local_filenames_lower:
                continue
            unresolved_fids.append(fid)

        # Batch resolve metadata in browser context (chunks of 25)
        if unresolved_fids:
            chunk_size = 25
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
                        }}
                    }}
                    return JSON.stringify(out);
                }})()"""
                escaped_batch_js = batch_js.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                raw_res = arc_eval(escaped_batch_js)
                try:
                    batch_data = json.loads(raw_res)
                    if isinstance(batch_data, str):
                        batch_data = json.loads(batch_data)
                    for id_str, m in batch_data.items():
                        if id_str in course_files:
                            course_files[id_str]["meta"] = m
                except Exception:
                    pass

        for fid, finfo in course_files.items():
            meta = finfo.get("meta")
            title = finfo.get("title")
            filename = (meta.get("display_name") or meta.get("filename")) if meta else title
            if not filename:
                continue
            canvas_size = meta.get("size") if meta else None
            canvas_url = meta.get("url") if meta else None

            # Check if file exists locally by filename or exact byte size
            matched_local = local_filenames_lower.get(filename.lower())
            if not matched_local and canvas_size and canvas_size > 5000:
                # Avoid re-downloading files that were simply renamed locally
                if canvas_size in local_sizes:
                    matched_local = local_sizes[canvas_size]

            if matched_local:
                # If notebook or code was executed locally, size differences are normal — skip overwriting
                if filename.lower().endswith(('.ipynb', '.py')) or (canvas_size and matched_local["size"] == canvas_size) or canvas_size is None:
                    continue
                # If size differs on a non-code file (e.g. updated prelim/syllabus), update it!
                if canvas_size and matched_local["size"] != canvas_size:
                    if canvas_url:
                        differentials.append((canvas_url, matched_local["full_path"], meta, folder))
                    continue

            # Skip small non-document announcement icons
            if filename.lower() in ['image.png', 'images.jpeg'] and canvas_size and canvas_size < 500000 and "announcement" in finfo["source"].lower():
                continue

            if not canvas_url:
                continue

            dest_path = target_dest_for_file(folder, filename, finfo["source"])
            differentials.append((canvas_url, dest_path, meta, folder))

    # 4. Check Downloads folder for recent course materials
    downloads_proposal = os.path.join(DOWNLOADS_DIR, "Replication Project Part 1 Proposal, Due 1028.pdf")
    dest_proposal = os.path.join(REPO_ROOT, "SS1-ECON5021-AdvEconometrics1/Replication_Project/Replication Project Part 1 Proposal, Due 1028.pdf")
    if os.path.exists(downloads_proposal) and not os.path.exists(dest_proposal):
        differentials.append(("file://" + downloads_proposal, dest_proposal, {"display_name": os.path.basename(downloads_proposal)}, "SS1-ECON5021-AdvEconometrics1"))

    print("\n" + "=" * 60)
    print(f"DIFFERENTIALS FOUND: {len(differentials)} new course files")
    print("=" * 60)
    for url, dest, meta, fld in differentials:
        print(f"  + [{fld}] {os.path.basename(dest)} -> {os.path.relpath(dest, REPO_ROOT)}")

    if dry_run or not differentials:
        if dry_run:
            print("\nDry-run mode: no files downloaded or committed.")
        else:
            print("\nAll course materials are up to date! Nothing to download.")
        return

    # 5. Download differentials
    created_paths = []
    print("\nDownloading new course materials...")
    for url, dest, meta, fld in differentials:
        try:
            if url.startswith("file://"):
                src_path = url[7:]
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src_path, dest)
                print(f"  Organized: {os.path.basename(dest)} -> {os.path.relpath(dest, REPO_ROOT)}")
            else:
                download_file_to(url, dest)
            created_paths.append(os.path.relpath(dest, REPO_ROOT))
        except Exception as e:
            print(f"  [ERROR] Failed to save {os.path.basename(dest)}: {e}")

    # 6. Commit & Push if requested
    if push and created_paths:
        print("\n" + "=" * 60)
        print("Committing and pushing following AGENTS.md rules...")
        print("=" * 60)
        # Stage only created paths
        subprocess.run(["git", "add", "--"] + created_paths, cwd=REPO_ROOT, check=True)
        # Commit once per prompt
        msg = "Canvas sync: update course materials from Canvas"
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sync Canvas course differentials to MSQE_Stuff")
    parser.add_argument("--dry-run", action="store_true", help="Scan and list differences without downloading")
    parser.add_argument("--push", action="store_true", help="Automatically commit and push added materials according to AGENTS.md")
    args = parser.parse_args()
    run_sync(dry_run=args.dry_run, push=args.push)
