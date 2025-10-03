from setuptools import setup, find_packages

setup(
    name="terminal-game-manager",
    version="1.0.0",
    author="Your Name",
    description="Terminal Game Manager - Steam for terminal games",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tgm=tgm.main:main",
        ],
    },
    python_requires=">=3.7",
)
