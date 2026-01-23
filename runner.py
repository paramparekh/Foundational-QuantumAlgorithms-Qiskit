import subprocess
import os

target_dir = os.getcwd()
repo_url = "https://github.com/paramparekh/Foundational-QuantumAlgorithms-Qiskit.git"

def run_command(cmd, desc):
    print(f"--- {desc} ---")
    try:
        if cmd[0] == "pip":
            cmd = ["python", "-m", "pip"] + cmd[1:]
            
        result = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"Failed: {desc}")
            if "git" in cmd and ("already exists" in result.stderr or "File exists" in result.stderr):
                 return True
            return False
        return True
    except Exception as e:
        print(f"Exception during {desc}: {e}")
        return False

steps = [
    (["pip", "install", "-r", "requirements.txt"], "Installing Requirements"),
    (["python", "generate_report.py"], "Generating Report"),
    (["git", "init"], "Git Init"),
    (["git", "remote", "remove", "origin"], "Git Remote Remove (Clean)"), 
    (["git", "remote", "add", "origin", repo_url], "Git Remote Add"),
    (["git", "branch", "-M", "main"], "Git Branch Main"),
    (["git", "add", "."], "Git Add All"),
    (["git", "commit", "-m", "Project2 Implementation of Quantum Algorithms"], "Git Commit"),
    (["git", "push", "-u", "origin", "main", "--force"], "Git Push Force") 
]

for cmd, desc in steps:
    if desc == "Git Remote Remove (Clean)":
        subprocess.run(cmd, cwd=target_dir, capture_output=True) 
        continue
        
    success = run_command(cmd, desc)
    if not success:
        if "Git Commit" in desc:
            continue
        if "Installing" in desc or "Generating" in desc:
            print("Critical step failed. Stopping.")
            break
