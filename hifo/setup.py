from setuptools import setup, find_packages

setup(
    name="hifo",
    version="0.1",
    author="Shi Group, XJTU",
    description="HiFo-Prompt: Prompting with Hindsight and Foresight for LLM-based Automatic Heuristic Design",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.21.0,<2.0.0",  # 关键修改：严格锁定NumPy 1.x版本范围
        "numba",
        "joblib",
        "scikit-learn>=1.2.0,<1.4.0",  # 新增：兼容性约束，确保与NumPy 1.x兼容
        "pandas>=1.5.0,<2.2.0"  # 新增：兼容性约束，确保与NumPy 1.x兼容
    ],
    test_suite="tests"
)
