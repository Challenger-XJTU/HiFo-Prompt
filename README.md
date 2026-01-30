<div align=center>
<h1 align="center">
HiFo-Prompt: Prompting with Hindsight and Foresight
</h1>
<h3 align="center">
A Framework for LLM-based Automatic Heuristic Design with Evolutionary Navigator and Insight Pool
</h3>
Chinese Version 中文版本
![Github-image](https://img.shields.io/badge/github-12100E.svg?style=flat-square)

![License-image](https://img.shields.io/badge/License-MIT-orange?style=flat-square)

![Releases-image](https://img.shields.io/badge/Release-Version_1.0-blue?style=flat-square)

![Wiki-image](https://img.shields.io/badge/Docs-Documentation-black?style=flat-square)
</div>
<br>
[!Important]
HiFo-Prompt represents the next generation of LLM-based AHD, addressing the lack of global control and knowledge accumulation in previous methods like EoH and ReEvo.
A Platform for Evolutionary Computation + Large Language Model with Self-Evolving Knowledge and Adaptive Control.
<img src="./docs/figures/framework.jpg" alt="hifo_framework" width="800" height="auto" div align=center>
News 🔥
2025.8 🎉🎉 HiFo-Prompt has been released! It achieves state-of-the-art performance on TSP, Online BPP, and FSSP, significantly outperforming EoH and ReEvo in both solution quality and convergence speed.
2025.8, The paper HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design has been uploaded to Arxiv!
2025.8, We have released the code for Bayesian Optimization (Cost-aware Acquisition Functions), demonstrating HiFo's capability in continuous optimization tasks.
Introduction 📖
While LLM-based Automatic Heuristic Design (AHD) has shown promise, existing methods suffer from two main limitations: the use of static operators (lack of Foresight) and the inability to reuse learned principles (lack of Hindsight).
HiFo-Prompt introduces a novel framework that synergizes two key strategies:
Foresight (Evolutionary Navigator): Acts as a high-level meta-controller that monitors population dynamics (e.g., stagnation, diversity). It adaptively switches the search strategy between Explore, Exploit, and Balance regimes.
Hindsight (Insight Pool): Builds a persistent knowledge base by distilling successful design principles from elite heuristics. This transforms transient discoveries into reusable knowledge, preventing the LLM from "reinventing the wheel."
<img src="./docs/figures/convergence.jpg" alt="convergence" width="1000" height="auto" div align=center>
HiFo-Prompt demonstrates remarkable sample efficiency. As shown in the figure above, it converges significantly faster than EoH and ReEvo, often finding superior solutions with only 200 LLM requests.
If you find HiFo-Prompt helpful for your research or applied projects:
code
Bibtex
@article{chen2025hifo,
  title={HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design},
  author={Chen, Chentong and Zhong, Mengyuan and Sun, Jianyong and Fan, Ye and Shi, Jialong},
  journal={arXiv preprint arXiv:2508.13333},
  year={2025}
}
If you are interested in HiFo-Prompt, you can:
Contact us through email (see paper).
Submit an issue if you encounter any difficulty.
Requirements
python >= 3.10
numba
numpy
scikit-learn
joblib
HiFo-Prompt Example Usage 💻
Step 1: Install HiFo
We suggest install and run HiFo in conda env with python>=3.10
code
Bash
cd hifo

pip install .
Step 2: Try Example:
<span style="color: red;">Setup your Endpoint and Key for remote LLM or Setup your local LLM before start !</span>
For example, set the llm_api_endpoint to "dashscope.aliyuncs.com" (for Qwen), set llm_api_key to "your key", and set llm_model to "qwen-2.5-max".
code
Python
from hifo import hifo
from hifo.utils.getParas import Paras

# Parameter initilization #
paras = Paras() 

# Set parameters #
paras.set_paras(method = "hifo",    # ['eoh','hifo']
                problem = "tsp_construct", #['tsp_construct','bp_online', 'fssp_gls']
                llm_api_endpoint = "xxx", # set your LLM endpoint
                llm_api_key = "xxx",   # set your LLM key
                llm_model = "qwen-max",
                ec_pop_size = 4, # HiFo works well with small populations
                ec_n_pop = 8,  # number of generations
                exp_n_proc = 4,  # multi-core parallel
                exp_debug_mode = False)

# initilization
evolution = hifo.EVOL(paras)

# run 
evolution.run()
HiFo uses Step-by-Step Construction strategies to evolve superior node selection heuristics.
code
Bash
cd examples/tsp_construct

python runHiFo.py
(<span style="color: red;">Beat state-of-the-art handcrafted heuristics (Best Fit) and LLM-based methods (EoH) with fewer queries!</span>)
code
Bash
cd examples/bp_online

python runHiFo.py
Evolving the Edge Update Strategy for Guided Local Search.
code
Bash
cd examples/fssp_gls

python runHiFo.py
More Examples using HiFo-Prompt Platform
Area	Problem	Paper	Code
Combinatorial Optimization	Online Bin Packing, scoring function	paper	code
TSP, construct heuristic	paper	code
TSP, guided local search (GLS)	paper	code
Flow Shop Scheduling Problem (FSSP), GLS	paper	code
Bayesian Optimization	Cost-aware Acquisition Function Design	paper	code
LLMs
Remote LLM + API (e.g., Qwen-2.5, GPT-4o, Deepseek) (Recommended !):
Qwen (Alibaba): Recommended in the paper for high performance.
OpenAI API.
Deepseek API.
Local LLM Deployment:
Similar to EoH, HiFo supports local deployment via vLLM or HuggingFace text-generation-inference.
Simply configure the url in your parameter settings.
Contributors
<img src="https://github.com/chentong-chen.png" width="60" div align=center> Chentong Chen
<img src="https://github.com/my-zhong.png" width="60" div align=center> Mengyuan Zhong
<img src="https://github.com/jialong-shi.png" width="60" div align=center> Jialong Shi
