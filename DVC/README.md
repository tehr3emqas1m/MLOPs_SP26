
[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-13ADC7?style=flat&logo=dvc)](https://dvc.org/)
[![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?style=flat&logo=git)](https://git-scm.com/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat&logo=python)](https://python.org/)


# Data Version Control (DVC)

**DVC (Data Version Control)** is an open-source tool that helps track and manage **datasets, machine learning models, and ML pipelines** in the same way Git tracks source code.

It stores large files (data/models) outside Git while keeping lightweight references to them inside the repository.

### Why is DVC Needed?

Git works well for code but struggles with:

* Large datasets
* Machine learning models
* Frequent changes to data files

DVC solves this by:

* **Versioning datasets and models** just like code.
* **Tracking experiments** and their results.
* **Enabling reproducibility**, so others can recreate the same training process.
* **Reducing repository size** by storing large files in remote storage (e.g., cloud storage, shared servers).
* **Facilitating team collaboration** on data-heavy projects.

### Example

Without DVC:

```text
Git → code only
dataset.csv (2 GB) → difficult to manage
```

With DVC:

```text
Git → code + dataset metadata
DVC → actual dataset storage and versioning


# DVC Example Project: Salary Prediction with Versioned Datasets

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

