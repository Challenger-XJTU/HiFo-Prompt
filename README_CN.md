<div align="center">

<h1 align="center">HiFo-Prompt</h1>

<h3 align="center">基于回顾与前瞻提示的大模型自动启发式算法设计</h3>

<p align="center">
<strong>🧠 回顾式洞察池 (Insight Pool)</strong> · <strong>🔭 前瞻式演化导航器 (Navigator)</strong> · <strong>🔄 闭环进化</strong>
</p>

![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Release](https://img.shields.io/badge/Release-v1.0.0-green?style=flat-square)

[English](./README.md) · [中文 (Chinese)](./README_CN.md)

</div>

<br/>

## 📢 新闻

- **2026 年 1 月**：🎉 HiFo-Prompt:基于回顾与前瞻提示的大模型自动启发式算法设计 被 **ICLR 2026** 接收为 Poster！

<br/>

## 📖 简介

**HiFo-Prompt**（Hindsight-Foresight Prompt，回顾-前瞻提示）是一个创新的**自动启发式算法设计（AHD）**框架，将**大语言模型（LLM）**与**进化计算（EC）**协同结合。

现有的基于 LLM 的方法通常存在*短期记忆*（遗忘成功的技巧）和*缺乏方向*（随机搜索无策略）的问题。HiFo-Prompt 通过引入两个关键机制解决了这些问题：

- **🧠 回顾（Insight Pool 洞察池）**：一个自我进化的知识库，从高性能启发式算法中提炼和存储"设计原则"，避免系统重复发明轮子。

- **🔭 前瞻（Evolutionary Navigator 演化导航器）**：一个元控制器，监控种群动态（停滞、多样性），并通过特定的**设计指令（Design Directive）**主动切换搜索策略（*探索 Explore*、*利用 Exploit* 或 *平衡 Balance*）。

<br/>

## 🔥 核心特性

| 组件 | 功能 | 重要性 |
|------|------|--------|
| **Insight Pool（洞察池）** | 提取并复用知识 | 不再丢弃父代，而是提取它们*成功的原因*。提示词中注入经过验证的"洞察"。 |
| **Evolutionary Navigator（演化导航器）** | 自适应控制 | 检测搜索是否陷入停滞或过于狭窄（低多样性），动态调整提示策略。 |
| **解耦评估** | 高效流程 | 将"思考"与"代码"解耦，相比标准方法实现更快的迭代和更低的 Token 消耗。 |

<br/>

## 🛠️ 安装

我们推荐使用 **Conda** 管理环境。

```bash
# 1. 创建环境
conda create -n hifo python=3.10
conda activate hifo

# 2. 克隆仓库
git clone https://github.com/FeiLiu36/HiFo.git
cd HiFo

# 3. 安装依赖
cd hifo
pip install -e .
```

<br/>

## 🚀 快速开始

> **注意**：您必须拥有 LLM API 密钥（如 OpenAI、DeepSeek、Qwen）或运行本地 LLM 服务器。

### 1. 基本使用结构

```python
from hifo import hifo
from hifo.utils.getParas import Paras

# 1. 初始化参数
paras = Paras() 

# 2. 配置 HiFo
paras.set_paras(
    method = "hifo",               
    problem = "tsp_construct",          # 问题类型: 'tsp_construct', 'bp_online'
    llm_api_endpoint = "api.deepseek.com", # 您的 API 端点
    llm_api_key = "sk-xxxxxxxx",        # 您的 API 密钥
    llm_model = "deepseek-chat",        # 模型名称
    ec_pop_size = 4,                    # 种群大小（推荐: 4-8）
    ec_n_pop = 10,                      # 进化代数
    exp_n_proc = 4,                     # 评估并行线程数
    exp_debug_mode = False              # 设为 True 可查看提示构建详情
)

# 3. 初始化并运行
evolution = hifo.EVOL(paras)
evolution.run()
```

### 2. 运行示例

我们为标准组合优化问题提供了即用型脚本。

#### 旅行商问题（TSP）

为 TSP 设计构造式启发式算法。

```bash
cd examples/tsp_construct
python runHiFo.py
```

#### 在线装箱问题（BPP）

为在线装箱设计评分函数。

```bash
cd examples/bp_online
python runHiFo.py
```

#### 自定义问题

```bash
cd examples/user_XXX
python runHiFo.py
```

<br/>

## ⚙️ 大模型配置

HiFo-Prompt 支持**远程 API** 和**本地 LLM 部署**两种方式。

### 方式 A：远程 API（推荐）

支持协议：OpenAI 兼容 API（DeepSeek、Moonshot、ChatGPT 等）。

修改 `runHiFo.py`：

```python
llm_api_endpoint = "api.openai.com" 
llm_api_key = "your_key"
llm_model = "gpt-4o"
```

### 方式 B：本地 LLM（vLLM / HuggingFace）

1. 启动本地服务器（例如使用 vLLM）：

```bash
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct --port 8000
```

2. 配置 HiFo：

```python
llm_use_local = True
llm_local_url = "http://localhost:8000/v1/chat/completions"
```

<br/>

## 📂 项目结构

```
HiFo-Prompt/
├── hifo/
│   ├── src/hifo/
│   │   ├── methods/
│   │   │   └── hifo/
│   │   │       ├── hifo.py                   # HiFo 主算法
│   │   │       ├── hifo_evolution.py         # 进化算子 (i1, e1, m1 等)
│   │   │       ├── insight_pool.py           # 🧠 回顾模块
│   │   │       └── evolutionary_navigator.py # 🔭 前瞻模块（策略控制）
│   │   ├── llm/                              # LLM 接口
│   │   ├── problems/                         # 问题定义
│   │   └── utils/                            # 参数解析与工具函数
│   └── setup.py
├── examples/                                 # 问题专用运行脚本（TSP、BPP 等）
└── docs/                                     # 文档与教程
```

<br/>

## 📊 配置参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `method` | 算法方法（`hifo`, `ael`） | `hifo` |
| `problem` | 问题类型 | `tsp_construct` |
| `ec_pop_size` | 每代种群大小 | `5` |
| `ec_n_pop` | 进化代数 | `5` |
| `exp_n_proc` | 并行进程数 | `1` |
| `eva_timeout` | 评估超时时间（秒） | `500` |
| `exp_debug_mode` | 启用调试输出 | `False` |

<br/>

## 📜  社区与引用

我们正在积极维护 HiFo-Prompt，非常期待听到社区的声音！
- 遇到问题？ 如果您在使用中发现 Bug 或有功能建议，请查看 Issues 页面或提交新问题。
- 寻求合作： 我们对 AHD 和 LLM 相关的探讨持开放态度。欢迎通过邮件或 PR 联系我们，让我们一起探索自动化算法设计的上限！🤝

支持我们： 如果 HiFo-Prompt 对您的研究有帮助，或者您喜欢我们的方法，请为本仓库 点亮 Star ⭐ 或 Fork 🍴。您的支持是我们更新的动力！

```bibtex
@article{hifo2025,
  title={HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design},
  author={Anonymous},
  journal={Under Review},
  year={2025}
}
```

<br/>

## 📄 许可证

本项目采用 **MIT 许可证**。

---

<div align="center">

**[⬆ 返回顶部](#hifo-prompt)**

</div>
