<div align="center">
<h1 align="center">
HiFo-Prompt
</h1>
<h3 align="center">
Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design
</h3>
<p align="center">
<strong>🧠 Hindsight Insight Pool</strong> · <strong>🔭 Foresight Evolutionary Navigator</strong> · <strong>🔄 Closed-Loop Evolution</strong>
</p>
![License-image](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)

![Python-image](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)

![Releases-image](https://img.shields.io/badge/Release-v1.0.0-green?style=flat-square)
English · 中文 (Chinese)
</div>
<br/>
📖 Introduction
HiFo-Prompt (Hindsight-Foresight Prompt) is a novel framework for Automatic Heuristic Design (AHD) that synergizes Large Language Models (LLMs) with Evolutionary Computation (EC).
Existing LLM-based methods often suffer from short-term memory (forgetting successful tricks) and lack of direction (randomly searching without a strategy). HiFo-Prompt solves this by introducing two key mechanisms:
Hindsight (The Insight Pool): A self-evolving knowledge base that distills and stores "design principles" from high-performing heuristics, preventing the system from reinventing the wheel.
Foresight (The Evolutionary Navigator): A meta-controller that monitors population dynamics (stagnation, diversity) and actively switches search regimes (Explore, Exploit, or Balance) via specific design directives.
<div align="center">
<img src="./docs/figures/framework.jpg" alt="HiFo Framework Diagram" width="800">
<br>
<em>Overview of the HiFo-Prompt Framework</em>
</div>
🔥 Key Features
Component	Function	Why it matters
Insight Pool	Extracts & Reuses Knowledge	Instead of discarding parents, we extract why they worked. The prompts are augmented with proven "Insights".
Evolutionary Navigator	Adaptive Control	Detects if the search is stuck (stagnation) or too narrow (low diversity) and dynamically adjusts the prompt strategy.
Decoupled Evaluation	Efficient Pipeline	Decouples "Thought" from "Code", allowing for faster iteration and lower token consumption compared to standard methods.
🛠️ Installation
We recommend using Conda to manage the environment.
code
Bash
# 1. Create environment
conda create -n hifo python=3.10
conda activate hifo

# 2. Clone repository
git clone https://github.com/YourUsername/HiFo-Prompt.git
cd HiFo-Prompt

# 3. Install dependencies
pip install -e .
🚀 Quick Start
Note: You must have an LLM API key (e.g., OpenAI, DeepSeek, Qwen) or a local LLM server running.
1. Basic Usage Structure
code
Python
from hifo import hifo
from hifo.utils.getParas import Paras

# 1. Initialize Parameters
paras = Paras() 

# 2. Configure HiFo
paras.set_paras(
    method = "hifo",               
    problem = "tsp_construct",          # Problem: 'tsp_construct', 'bp_online', 'fssp'
    llm_api_endpoint = "api.deepseek.com", # Your API Endpoint
    llm_api_key = "sk-xxxxxxxx",        # Your API Key
    llm_model = "deepseek-chat",        # Model Name
    ec_pop_size = 4,                    # Population size (recommended: 4-8)
    ec_n_pop = 10,                      # Number of generations
    exp_n_proc = 4,                     # Parallel threads for evaluation
    exp_debug_mode = False              # Set True to see prompt construction details
)

# 3. Initialize & Run
evolution = hifo.EVOL(paras)
evolution.run()
2. Running Examples
We provide ready-to-run scripts for standard combinatorial optimization problems.
Traveling Salesman Problem (TSP)
Constructive heuristic design for TSP.
code
Bash
cd examples/tsp_construct
python runHiFo.py
Online Bin Packing (BPP)
Designing scoring functions for online packing.
code
Bash
cd examples/bp_online
python runHiFo.py
Flow Shop Scheduling (FSSP)
code
Bash
cd examples/fssp_gls
python runHiFo.py
⚙️ LLM Configuration
HiFo-Prompt supports both remote APIs and local LLM deployment.
Option A: Remote API (Recommended)
Supported protocols: OpenAI-compatible APIs (DeepSeek, Moonshot, ChatGPT, etc.).
Modify runHiFo.py:
code
Python
llm_api_endpoint = "api.openai.com" 
llm_api_key = "your_key"
llm_model = "gpt-4o"
Option B: Local LLM (vLLM / HuggingFace)
Start your local server (e.g., using vLLM):
code
Bash
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct --port 8000
Configure HiFo:
code
Python
llm_use_local = True
llm_local_url = "http://localhost:8000/v1/chat/completions"
📂 Project Structure
code
Code
HiFo-Prompt/
├── hifo/
│   ├── algorithms/
│   │   └── hifo_evolution.py    # Core Evolution Logic (i1, e1, m1 operators)
│   ├── components/
│   │   ├── insight_pool.py      # Hindsight Module
│   │   └── navigator.py         # Foresight Module (Regime Control)
│   ├── llm/                     # LLM Interfaces
│   └── utils/                   # Parameter parsing & helpers
├── examples/                    # Problem-specific runners (TSP, BPP, etc.)
├── docs/                        # Documentation & Tutorials
└── setup.py
📊 Performance
HiFo-Prompt achieves state-of-the-art results on standard benchmarks like TSP-GLS, Online BPP, and FSSP, often converging significantly faster than previous methods (EoH, ReEvo) due to the Evolutionary Navigator guiding the search.
(See our paper for detailed convergence curves and ablation studies.)
📜 Citation
If you find HiFo-Prompt useful for your research, please cite our work:
code
Bibtex
@article{hifo2025,
  title={HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design},
  author={Anonymous},
  journal={Under Review},
  year={2025}
}
📄 License
This project is licensed under the MIT License.
