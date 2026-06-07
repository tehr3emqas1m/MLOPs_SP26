# DVC Example Project: Salary Prediction with Versioned Datasets

[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-13ADC7?style=flat&logo=dvc)](https://dvc.org/)
[![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?style=flat&logo=git)](https://git-scm.com/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat&logo=python)](https://python.org/)

## Project Overview

This project demonstrates Data Version Control (DVC) by simulating a real-world scenario where a dataset grows incrementally over time. We create synthetic salary data based on years of experience and train linear regression models on progressively larger datasets.

### What You'll Learn

- Track datasets with DVC (not Git)
- Version large files efficiently
- Train models on different dataset versions
- Reproduce results across dataset versions
- Understand the difference between Git (code) and DVC (data)

### Dataset Evolution

| Version | Rows | Description |
|---------|------|-------------|
| v1 | 500 | Initial dataset |
| v2 | 1000 | Added 500 more rows |
| v3 | 1500 | Complete dataset |

## Project Structure

