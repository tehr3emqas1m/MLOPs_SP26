# Great Expectations - Data Quality Validation

## What is Great Expectations?

**Great Expectations (GX)** is an open-source Python framework that helps you define, test, and document data quality rules. Think of it as unit tests for your data - catching bad data before it breaks your ML models or analytics pipelines.

## Why It Matters in MLOps

Bad data equals bad models. Great Expectations sits at the beginning of your ML pipeline, ensuring only high-quality data reaches your training and inference systems.

## What This Demo Shows

The notebook (`great_expectations.ipynb`) in this folder demonstrates a complete GX workflow:

### 1. Generate Test Data
- `perfect_employee_data.csv` - Clean data following all rules
- `faulty_employee_data.csv` - Data with intentional violations (negative experience, impossibly low salary)

### 2. Define Expectations (Rules)
- employee_id must not be null
- experience_years must be between 0-40
- salary must be between 30,000-150,000
- department must be in Sales, Engineering, HR, or Marketing

### 3. Validate and Report
- Perfect data: All expectations pass
- Faulty data: GX identifies exact violations:
  - experience_years = -5 (fails range check)
  - salary = 500 (fails minimum salary check)

## Key GX Concepts Demonstrated

| Concept | What It Does |
|---------|---------------|
| Context | Central manager for GX environment |
| Expectation Suite | Collection of data quality rules |
| Validation Definition | Ties data and rules together |
| Batch | The actual data being validated |

```

## Expected Output

```
Perfect data — Validation successful: True
Faulty data — Validation successful: False

Failed expectations:
  - expect_column_values_to_be_between on column 'experience_years'
  - expect_column_values_to_be_between on column 'salary'
```

## Next Steps

- Add custom expectations for your own data
- Integrate with Airflow for pipeline validation
- Use with DVC to validate versioned datasets
- Connect to MLflow for experiment tracking
```
