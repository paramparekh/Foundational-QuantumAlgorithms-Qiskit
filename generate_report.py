import os
import subprocess
import datetime

# List of scripts to run
scripts = [
    "simon.py",
    "deutsch_jozsa.py",
    "grover.py",
    "qrng.py",
    "qkd_bb84.py"
]

def run_scripts():
    print("Running quantum algorithms...")
    for script in scripts:
        print(f"Executing {script}...")
        try:
            subprocess.run(["python", script], check=True)
            print(f"Finished {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")

def generate_html():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foundational Quantum Algorithms Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max_width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 2rem;
            text-align: center;
            border-radius: 8px 8px 0 0;
            margin-bottom: 2rem;
        }}
        h1 {{ margin: 0; font-size: 2.5rem; }}
        h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 2rem; }}
        .section {{
            background: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .results-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-top: 1rem;
        }}
        .result-box {{
            flex: 1;
            min-width: 300px;
            text-align: center;
            border: 1px solid #eee;
            padding: 10px;
            border-radius: 4px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .description {{ margin-bottom: 1rem; color: #555; }}
        footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #777;
            font-size: 0.9rem;
        }}
        code {{
            background-color: #f1f1f1;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: Consolas, monospace;
        }}
    </style>
</head>
<body>

<header>
    <h1>Foundational Quantum Algorithms</h1>
    <p>Implementation & Results Report</p>
    <p style="font-size: 0.9rem; opacity: 0.8">{current_date}</p>
</header>

<div class="section">
    <h2>Project Overview</h2>
    <p>This project demonstrates the implementation of five foundational quantum algorithms using <strong>Qiskit</strong>. 
    The algorithms selected cover quantum oracles, search, randomness generation, and key distribution.</p>
</div>

<div class="section">
    <h2>1. Simon's Algorithm</h2>
    <p class="description">
        Simon's algorithm solves a black-box problem exponentially faster than any classical algorithm. 
        Given a function f(x) such that f(x) = f(y) iff x ⊕ y ∈ {{0, s}}, the goal is to find the hidden string s.
    </p>
    <div class="results-container">
        <div class="result-box">
            <h3>Circuit Diagram</h3>
            <img src="simon_circuit.png" alt="Simon's Circuit">
        </div>
        <div class="result-box">
            <h3>Measurement Results</h3>
            <img src="simon_hist.png" alt="Simon's Histogram">
            <p>The results show bitstrings z such that z·s = 0 (mod 2).</p>
        </div>
    </div>
</div>

<div class="section">
    <h2>2. Deutsch-Jozsa Algorithm</h2>
    <p class="description">
        The Deutsch-Jozsa algorithm determines whether a given oracle function is constant or balanced with a single query,
        showcasing quantum parallelism.
    </p>
    <div class="results-container">
        <div class="result-box">
            <h3>Circuit Diagram</h3>
            <img src="dj_circuit.png" alt="Deutsch-Jozsa Circuit">
        </div>
        <div class="result-box">
            <h3>Measurement Results</h3>
            <img src="dj_hist.png" alt="Deutsch-Jozsa Histogram">
            <p>Measuring '00...0' indicates a Constant function; any other result indicates Balanced.</p>
        </div>
    </div>
</div>

<div class="section">
    <h2>3. Grover's Search Algorithm</h2>
    <p class="description">
        Grover's algorithm provides a quadratic speedup for searching unsorted databases. It amplifies the amplitude of the target state.
    </p>
    <div class="results-container">
        <div class="result-box">
            <h3>Circuit Diagram</h3>
            <img src="grover_circuit.png" alt="Grover's Circuit">
        </div>
        <div class="result-box">
            <h3>Measurement Results</h3>
            <img src="grover_hist.png" alt="Grover's Histogram">
            <p>High probability peak at the target state.</p>
        </div>
    </div>
</div>

<div class="section">
    <h2>4. Quantum Random Number Generation (QRNG)</h2>
    <p class="description">
        QRNG exploits the inherent probabilistic nature of quantum measurement (collapsing simple superposition states) 
        to generate true random numbers.
    </p>
    <div class="results-container">
        <div class="result-box">
            <h3>Circuit Diagram</h3>
            <img src="qrng_circuit.png" alt="QRNG Circuit">
        </div>
        <div class="result-box">
            <h3>Distribution</h3>
            <img src="qrng_hist.png" alt="QRNG Histogram">
            <p>Uniform distribution over all possible bitstrings.</p>
        </div>
    </div>
</div>

<div class="section">
    <h2>5. Quantum Key Distribution (BB84)</h2>
    <p class="description">
        The BB84 protocol allows two parties to securely share a key. This simulation demonstrates the sifting process 
        where bases match.
    </p>
    <div class="results-container">
        <div class="result-box">
            <h3>Key Sifting Efficiency</h3>
            <img src="bb84_stats.png" alt="BB84 Statistics">
            <p>Comparison of initial measured bits vs sifted key length (approx 50%).</p>
        </div>
    </div>
</div>

<footer>
    <p>Project implemented on Qiskit | Deployed via GitHub Pages</p>
</footer>

</body>
</html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Report generated: index.html")

if __name__ == "__main__":
    run_scripts()
    generate_html()
