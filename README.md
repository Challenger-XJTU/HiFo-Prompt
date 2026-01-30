<div align="center">

# HiFo: Hierarchical and Feedback-driven Optimization

### Automatic Algorithm Design with LLM-powered Evolutionary Computation

<p align="center">
  <strong>Insight Pool</strong> · <strong>Evolutionary Navigator</strong> · <strong>Feedback-driven Learning</strong>
</p>

[中文版本](./README_CN.md) · [Documentation](https://github.com/FeiLiu36/HiFo/tree/main/docs) · [Examples](./examples)

[![GitHub](https://img.shields.io/badge/GitHub-HiFo-181717?style=for-the-badge&logo=github)](https://github.com/FeiLiu36/HiFo)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-≥3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## Overview

**HiFo** is a cutting-edge framework that combines **Evolutionary Computation (EC)** with **Large Language Models (LLMs)** for automatic heuristic algorithm design. It introduces a novel **Insight Pool** mechanism that learns, stores, and leverages design principles throughout the evolutionary process.

### Why HiFo?

Traditional automatic algorithm design methods often lack the ability to accumulate and transfer knowledge across generations. HiFo addresses this limitation through:

| Feature | Description |
|---------|-------------|
| **Insight Pool** | Automatically extracts high-level design principles from successful algorithms and uses them to guide future generations |
| **Evolutionary Navigator** | Dynamically determines the search regime (exploration/exploitation/balanced) and provides design directives based on real-time search progress |
| **Feedback-driven Learning** | Continuously refines insights based on their actual effectiveness in producing high-quality solutions |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          HiFo Framework                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │   LLM API    │◄──►│  Evolution   │◄──►│  Evaluation  │     │
│   │  (GPT/etc.)  │    │   Engine     │    │    Module    │     │
│   └──────────────┘    └──────┬───────┘    └──────────────┘     │
│                              │                                  │
│                              ▼                                  │
│          ┌───────────────────────────────────────┐             │
│          │           HiFo-Prompt Layer           │             │
│          ├───────────────────┬───────────────────┤             │
│          │   Insight Pool    │    Navigator      │             │
│          │  ┌─────────────┐  │  ┌─────────────┐  │             │
│          │  │ Design Tips │  │  │   Regime    │  │             │
│          │  │ Feedback    │  │  │  Directive  │  │             │
│          │  └─────────────┘  │  └─────────────┘  │             │
│          └───────────────────┴───────────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Requirements

- Python ≥ 3.10
- NumPy
- Numba
- Joblib

### Quick Install

```bash
# Clone the repository
git clone https://github.com/FeiLiu36/HiFo.git
cd HiFo/hifo

# Install in development mode
pip install -e .
```

Or install directly:

```bash
cd hifo
pip install .
```

---

## Quick Start

### Basic Usage

```python
from hifo import hifo
from hifo.utils.getParas import Paras

# Initialize parameters
paras = Paras()

# Configure HiFo
paras.set_paras(
    method="hifo",
    problem="tsp_construct",         # Problem type
    llm_api_endpoint="api.deepseek.com",  # Your LLM API endpoint
    llm_api_key="your-api-key",      # Your API key
    llm_model="deepseek-chat",       # Model name
    ec_pop_size=8,                   # Population size
    ec_n_pop=10,                     # Number of generations
    exp_n_proc=4,                    # Parallel processes
    exp_debug_mode=False
)

# Run evolution
evolution = hifo.EVOL(paras)
evolution.run()
```

### Available Problems

| Problem | Description | Example Path |
|---------|-------------|--------------|
| `tsp_construct` | Constructive heuristic for TSP | `examples/tsp_construct/` |
| `bp_online` | Online Bin Packing | `examples/bp_online/` |
| Custom | Your own optimization problem | `examples/user_XXX/` |

---

## Examples

### Example 1: TSP Constructive Heuristic

```bash
cd examples/tsp_construct
python runHiFo.py
```

**Evaluate your evolved heuristic:**
```bash
cd examples/tsp_construct/evaluation
# Copy your heuristic to heuristic.py
python runEval.py
```

### Example 2: Online Bin Packing

```bash
cd examples/bp_online
python runHiFo.py
```

### Example 3: Custom Problem

Create your own problem by following the template in `examples/user_XXX/`.

---

## LLM Configuration

### Option 1: Remote LLM API (Recommended)

| Provider | Endpoint | Notes |
|----------|----------|-------|
| **DeepSeek** | `api.deepseek.com` | Cost-effective, good performance |
| **OpenAI** | `api.openai.com` | GPT-3.5/4 |
| **Other** | Various | See [API providers](#api-providers) |

### Option 2: Local LLM Deployment

1. Download a model from HuggingFace:
   ```bash
   git clone https://huggingface.co/google/gemma-2b-it
   ```

2. Start the local server:
   ```bash
   cd llm_server
   python gemma_instruct_server.py
   ```

3. Configure HiFo to use local endpoint:
   ```python
   paras.set_paras(
       llm_use_local=True,
       llm_local_url="http://127.0.0.1:11012/completions",
       ...
   )
   ```

### API Providers

- [DeepSeek API](https://platform.deepseek.com/) - Recommended
- [OpenAI API](https://openai.com/api/)
- [API2D](https://www.api2d.com/)

---

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `method` | Algorithm method (`hifo`, `ael`) | `hifo` |
| `problem` | Problem type | `tsp_construct` |
| `ec_pop_size` | Population size per generation | `5` |
| `ec_n_pop` | Number of generations | `5` |
| `exp_n_proc` | Number of parallel processes | `1` |
| `eva_timeout` | Evaluation timeout (seconds) | `500` |
| `exp_debug_mode` | Enable debug output | `False` |

---

## Project Structure

```
hifo/
├── src/hifo/
│   ├── methods/
│   │   └── hifo/
│   │       ├── hifo.py              # Main HiFo algorithm
│   │       ├── hifo_interface_EC.py # EC interface
│   │       ├── hifo_evolution.py    # Evolution operators
│   │       ├── insight_pool.py           # Insight Pool implementation
│   │       └── evolutionary_navigator.py # Evolutionary Navigator
│   ├── llm/                         # LLM interfaces
│   ├── problems/                    # Problem definitions
│   └── utils/                       # Utilities
├── examples/                        # Example applications
└── setup.py
```

---

## Citation

If you use HiFo in your research, please cite:

```bibtex
@inproceedings{hifo2025,
  title={HiFo: Hierarchical and Feedback-driven Optimization for Automatic Algorithm Design},
  author={},
  booktitle={},
  year={2025}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

**[Back to Top](#hifo-hierarchical-and-feedback-driven-optimization)**

</div>
