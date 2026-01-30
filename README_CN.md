<div align="center">

# HiFo：层次化反馈驱动优化框架

### 基于大语言模型驱动的进化计算自动算法设计平台

<p align="center">
  <strong>Insight Pool 洞察池</strong> · <strong>Evolutionary Navigator 演化导航器</strong> · <strong>反馈驱动学习</strong>
</p>

[English Version](./README.md) · [文档](https://github.com/FeiLiu36/HiFo/tree/main/docs) · [示例](./examples)

[![GitHub](https://img.shields.io/badge/GitHub-HiFo-181717?style=for-the-badge&logo=github)](https://github.com/FeiLiu36/HiFo)
[![License](https://img.shields.io/badge/许可证-MIT-green?style=for-the-badge)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-≥3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

</div>

---

## 概述

**HiFo** 是一个前沿的自动算法设计框架，将**进化计算（EC）**与**大语言模型（LLM）**相结合。该框架创新性地引入了 **Insight Pool（洞察池）**机制，能够在进化过程中学习、存储和利用设计原则。

### 为什么选择 HiFo？

传统的自动算法设计方法通常缺乏跨代际积累和迁移知识的能力。HiFo 通过以下特性解决了这一局限：

| 特性 | 描述 |
|------|------|
| **Insight Pool（洞察池）** | 自动从成功的算法中提取高层设计原则，并用于指导后续代际的生成 |
| **Evolutionary Navigator（演化导航器）** | 基于实时搜索进度动态决定搜索策略（探索/利用/平衡），并提供设计指令 |
| **反馈驱动学习** | 根据洞察在生成高质量解决方案中的实际效果持续优化 |

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        HiFo 框架                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │   LLM API    │◄──►│    进化      │◄──►│    评估      │     │
│   │  (GPT等)     │    │    引擎      │    │    模块      │     │
│   └──────────────┘    └──────┬───────┘    └──────────────┘     │
│                              │                                  │
│                              ▼                                  │
│          ┌───────────────────────────────────────┐             │
│          │         HiFo-Prompt 提示层            │             │
│          ├───────────────────┬───────────────────┤             │
│          │    Insight Pool   │    Navigator      │             │
│          │     洞察池        │    演化导航器     │             │
│          │  ┌─────────────┐  │  ┌─────────────┐  │             │
│          │  │  设计原则   │  │  │   Regime    │  │             │
│          │  │  效果反馈   │  │  │  Directive  │  │             │
│          │  └─────────────┘  │  └─────────────┘  │             │
│          └───────────────────┴───────────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 安装

### 环境要求

- Python ≥ 3.10
- NumPy
- Numba
- Joblib

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/FeiLiu36/HiFo.git
cd HiFo/hifo

# 开发模式安装
pip install -e .
```

或直接安装：

```bash
cd hifo
pip install .
```

---

## 快速开始

### 基本用法

```python
from hifo import hifo
from hifo.utils.getParas import Paras

# 初始化参数
paras = Paras()

# 配置 HiFo
paras.set_paras(
    method="hifo",
    problem="tsp_construct",              # 问题类型
    llm_api_endpoint="api.deepseek.com",  # LLM API 端点
    llm_api_key="your-api-key",           # API 密钥
    llm_model="deepseek-chat",            # 模型名称
    ec_pop_size=8,                        # 种群大小
    ec_n_pop=10,                          # 进化代数
    exp_n_proc=4,                         # 并行进程数
    exp_debug_mode=False
)

# 运行进化
evolution = hifo.EVOL(paras)
evolution.run()
```

### 支持的问题类型

| 问题 | 描述 | 示例路径 |
|------|------|----------|
| `tsp_construct` | TSP 构造式启发式 | `examples/tsp_construct/` |
| `bp_online` | 在线装箱问题 | `examples/bp_online/` |
| 自定义 | 您自己的优化问题 | `examples/user_XXX/` |

---

## 使用示例

### 示例 1：TSP 构造式启发式

```bash
cd examples/tsp_construct
python runHiFo.py
```

**评估进化出的启发式算法：**
```bash
cd examples/tsp_construct/evaluation
# 将您的启发式代码复制到 heuristic.py
python runEval.py
```

### 示例 2：在线装箱问题

```bash
cd examples/bp_online
python runHiFo.py
```

### 示例 3：自定义问题

参考 `examples/user_XXX/` 中的模板创建您自己的问题。

---

## 大模型配置

### 方式一：远程 LLM API（推荐）

| 服务商 | 端点 | 说明 |
|--------|------|------|
| **DeepSeek** | `api.deepseek.com` | 性价比高，性能优秀 |
| **OpenAI** | `api.openai.com` | GPT-3.5/4 |
| **其他** | 多种 | 见[API 服务商](#api-服务商) |

### 方式二：本地 LLM 部署

1. 从 HuggingFace 下载模型：
   ```bash
   git clone https://huggingface.co/google/gemma-2b-it
   ```

2. 启动本地服务：
   ```bash
   cd llm_server
   python gemma_instruct_server.py
   ```

3. 配置 HiFo 使用本地端点：
   ```python
   paras.set_paras(
       llm_use_local=True,
       llm_local_url="http://127.0.0.1:11012/completions",
       ...
   )
   ```

### API 服务商

- [DeepSeek API](https://platform.deepseek.com/) - 推荐
- [OpenAI API](https://openai.com/api/)
- [API2D](https://www.api2d.com/)

---

## 配置参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `method` | 算法方法（`hifo`, `ael`） | `hifo` |
| `problem` | 问题类型 | `tsp_construct` |
| `ec_pop_size` | 每代种群大小 | `5` |
| `ec_n_pop` | 进化代数 | `5` |
| `exp_n_proc` | 并行进程数 | `1` |
| `eva_timeout` | 评估超时时间（秒） | `500` |
| `exp_debug_mode` | 启用调试输出 | `False` |

---

## 项目结构

```
hifo/
├── src/hifo/
│   ├── methods/
│   │   └── hifo/
│   │       ├── hifo.py              # HiFo 主算法
│   │       ├── hifo_interface_EC.py # 进化计算接口
│   │       ├── hifo_evolution.py    # 进化算子
│   │       ├── insight_pool.py           # Insight Pool 实现
│   │       └── evolutionary_navigator.py # Evolutionary Navigator 演化导航器
│   ├── llm/                         # LLM 接口
│   ├── problems/                    # 问题定义
│   └── utils/                       # 工具函数
├── examples/                        # 示例应用
└── setup.py
```

---

## 引用

如果您在研究中使用了 HiFo，请引用：

```bibtex
@inproceedings{hifo2025,
  title={HiFo: Hierarchical and Feedback-driven Optimization for Automatic Algorithm Design},
  author={},
  booktitle={},
  year={2025}
}
```

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](./LICENSE) 文件。

---

<div align="center">

**[返回顶部](#hifo层次化反馈驱动优化框架)**

</div>
