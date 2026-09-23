"""Run the full replication pipeline in order: parse -> descriptives -> CL -> ML -> dashboard -> slide figures."""
import runpy
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["01_parse_data.py", "02_descriptives.py", "03_conditional_logit.py", "04_mixed_logit.py", "05_build_dashboard.py", "06_slide_figures.py"]

if __name__ == "__main__":
    for step in STEPS:
        t0 = time.time()
        print(f"\n{'=' * 78}\n>>> {step}\n{'=' * 78}")
        runpy.run_path(str(HERE / step), run_name="__main__")
        print(f"<<< {step} done in {time.time() - t0:.0f}s")
