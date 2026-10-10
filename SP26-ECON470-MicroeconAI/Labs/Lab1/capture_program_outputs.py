"""Capture labeled program outputs for lab submission (readable microols log)."""
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_capture(name: str, cmd: list[str], out_path: Path) -> None:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    header = (
        f"{'=' * 72}\n"
        f"LAB PROGRAM OUTPUT\n"
        f"Program: {name}\n"
        f"Command: {' '.join(cmd)}\n"
        f"Exit code: {proc.returncode}\n"
        f"Captured (UTC): {datetime.now(timezone.utc).isoformat()}\n"
        f"{'=' * 72}\n\n"
    )
    body = proc.stdout
    if proc.stderr:
        body += "\n--- stderr ---\n" + proc.stderr
    out_path.write_text(header + body, encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")


def summarize_microols(raw: str, out_path: Path) -> None:
    """microols uses \\r; split and keep first/last step + static tail."""
    parts = raw.replace("\r", "\n").split("\n")
    steps = [p.strip() for p in parts if p.strip().startswith("step ")]
    other = []
    skip_prefixes = ("num observations", "num params", "training for")
    for p in parts:
        t = p.strip()
        if not t or t.startswith("step "):
            continue
        if any(t.startswith(s) for s in skip_prefixes):
            continue
        other.append(t)

    summary = (
        f"{'=' * 72}\n"
        f"LAB PROGRAM OUTPUT (readable summary)\n"
        f"Program: microols.py\n"
        f"Note: Training prints {len(steps)} progress lines with carriage return (\\r).\n"
        f"Below: first step, last step, then final printed sections.\n"
        f"Captured (UTC): {datetime.now(timezone.utc).isoformat()}\n"
        f"{'=' * 72}\n\n"
    )
    # Header lines appear before the first "step ..." progress line
    header_done = False
    for p in parts:
        t = p.strip()
        if t.startswith("step "):
            header_done = True
        if not header_done and t and not t.startswith("step "):
            summary += t + "\n"
    summary += "\n"
    if steps:
        summary += "--- first training line ---\n" + steps[0] + "\n\n"
        summary += "--- last training line ---\n" + steps[-1] + "\n\n"
    summary += "--- remainder of stdout ---\n"
    summary += "\n".join(other) + "\n"
    out_path.write_text(summary, encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    p2 = ROOT / "program_output_problem2_ces.txt"
    run_capture("problem2_ces.py", [sys.executable, str(ROOT / "problem2_ces.py")], p2)

    proc = subprocess.run(
        [sys.executable, str(ROOT / "microols.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=600,
    )
    raw_path = ROOT / "program_output_microols_raw.txt"
    raw_header = (
        f"{'=' * 72}\n"
        f"LAB PROGRAM OUTPUT (raw stdout, includes \\r progress lines)\n"
        f"Program: microols.py\n"
        f"Exit code: {proc.returncode}\n"
        f"Captured (UTC): {datetime.now(timezone.utc).isoformat()}\n"
        f"{'=' * 72}\n\n"
    )
    raw_path.write_text(raw_header + proc.stdout + ("\n--- stderr ---\n" + proc.stderr if proc.stderr else ""), encoding="utf-8")
    print(f"Wrote {raw_path} ({raw_path.stat().st_size} bytes)")

    clean_path = ROOT / "program_output_microols.txt"
    summarize_microols(proc.stdout, clean_path)
