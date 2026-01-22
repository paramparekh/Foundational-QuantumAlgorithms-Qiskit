import subprocess
import os

# Target directory is NOW the current directory (Project2)
target_dir = os.getcwd()
repo_url = "https://github.com/paramparekh/Foundational-QuantumAlgorithms-Qiskit.git"

def run_command(cmd, desc):
    print(f"--- {desc} ---")
    try:
        # Run in current directory
        if cmd[0] == "pip":
            cmd = ["python", "-m", "pip"] + cmd[1:]
            
        result = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"Failed: {desc}")
            # Don't strictly return False for git init/remote errors if they already exist
            if "git" in cmd and ("already exists" in result.stderr or "File exists" in result.stderr):
                 return True
            return False
        return True
    except Exception as e:
        print(f"Exception during {desc}: {e}")
        return False

# Steps: Install -> Run Generator -> Git Init/Push
steps = [
    (["pip", "install", "-r", "requirements.txt"], "Installing Requirements"),
    (["python", "generate_report.py"], "Generating Report"),
    (["git", "init"], "Git Init"),
    (["git", "remote", "remove", "origin"], "Git Remote Remove (Clean)"), # cleaning potential old remote
    (["git", "remote", "add", "origin", repo_url], "Git Remote Add"),
    (["git", "branch", "-M", "main"], "Git Branch Main"),
    (["git", "add", "."], "Git Add All"),
    (["git", "commit", "-m", "Project2 Implementation of Quantum Algorithms"], "Git Commit"),
    (["git", "push", "-u", "origin", "main", "--force"], "Git Push Force") # Force push since we moved folders
]

for cmd, desc in steps:
    # Skip remote remove if init just happened (it might fail if not exists, so we ignore failure inside run_command logic? No, let's handle it)
    if desc == "Git Remote Remove (Clean)":
        subprocess.run(cmd, cwd=target_dir, capture_output=True) # Ignore output/error
        continue
        
    success = run_command(cmd, desc)
    if not success:
        # If commit fails (nothing to commit) continue
        if "Git Commit" in desc:
            continue
        # If push fails, we stop?
        if "Installing" in desc or "Generating" in desc:
            print("Critical step failed. Stopping.")
            break
