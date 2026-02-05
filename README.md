# COVID-19 Public Dataset Analysis (India)

**Ishak Islam** | UMID28072552431 | Unified Mentor Internship

## About

Analysis of COVID-19 pandemic data in India using public datasets. The analysis covers state-wise confirmed cases, deaths, recoveries, testing statistics, and vaccination progress across India from 2020 to 2021.

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_covid19_india_analysis.ipynb
```

Run all cells to see the analysis.

## Dataset

Download from: https://data.covid19india.org/

Required CSV files to place in `data/` folder:
- `states.csv` - State-wise time series data (https://data.covid19india.org/csv/latest/states.csv)
- `case_time_series.csv` - India daily time series (https://data.covid19india.org/csv/latest/case_time_series.csv)
- `state_wise_daily.csv` - State-wise daily data (https://data.covid19india.org/csv/latest/state_wise_daily.csv)
- `state_wise.csv` - State-wise cumulative data (https://data.covid19india.org/csv/latest/state_wise.csv)

## Files

```
├── data/           # Put dataset files here
├── notebooks/      # Analysis notebook
├── scripts/        # Helper functions
├── visualizations/ # Charts
├── tableau/        # Tableau exports
└── docs/           # Documentation
```

## Results

- State-wise COVID-19 case analysis
- Daily and cumulative trend analysis
- Testing rate comparison across states
- Vaccination progress tracking
- Recovery and mortality rate analysis
- Data exports ready for Tableau dashboards

## Tableau Dashboard

**Live Interactive Dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/ishak.islam/viz/COVID-19IndiaAnalysis_17703051952670/Dashboard?publish=yes)

## Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn, Tableau

## GitHub Repository

**Source Code:** [https://github.com/isacmj7/covid-19-public-dataset-analysis](https://github.com/isacmj7/covid-19-public-dataset-analysis)
