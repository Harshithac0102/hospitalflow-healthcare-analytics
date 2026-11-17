# HospitalFlow — Emergency Department Patient Flow Analytics

A reproducible exploratory analytics dashboard built around the Kaggle **healthcare_analytics_patient_flow_data** dataset by Hassan Jameel Ahmed.

## What it does
- Loads and validates the dataset's expected schema
- Reports patient visit counts, wait-time distribution, admission share, and referral patterns
- Explores recorded arrivals by hour and wait times by admission status
- Reports missing satisfaction data and ambiguous date formats
- Runs automated tests through GitHub Actions

## Dataset
Source: https://www.kaggle.com/search?q=healthcare_analytics_patient_flow_data

The CSV in `data/` is included for local development. Check the dataset's Kaggle license before publicly redistributing it. If redistribution is not permitted, remove the CSV from the public repository and document how users can download it themselves.

**Important:** The source contains mixed-looking date strings. For unambiguous DD/MM/YYYY dates, the loader converts them; for dates where both components are <=12, it assumes MM/DD/YYYY and flags them. Do not draw strong calendar conclusions until the source convention is confirmed.

## Run locally (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Limitations
This is exploratory operational analytics, not a clinical decision tool. No claims are made about staffing, bed capacity, or causality. The data's real-world provenance should be verified with its publisher. A simulation engine is planned but not implemented in this release.

## Roadmap
- Verify date encoding and provenance
- Add temporal train/test split and forecasting baselines where supported
- Add an explicitly assumption-driven discrete-event simulation
- Add sensitivity analysis and model monitoring
