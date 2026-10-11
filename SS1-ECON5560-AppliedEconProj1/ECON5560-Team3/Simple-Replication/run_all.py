# Runs the four steps in order. Step 4 takes a couple of minutes.
import subprocess
import sys

for script in ["step1_prepare_data.py", "step2_look_at_raw_choices.py",
               "step3_conditional_logit.py", "step4_mixed_logit.py"]:
    print(f"\n######## {script}")
    subprocess.run([sys.executable, script], check=True)
