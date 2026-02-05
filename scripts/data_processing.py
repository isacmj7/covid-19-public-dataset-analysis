"""
Data processing for COVID-19 India analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_states_data(filepath=None):
    """Load state-wise time series data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "states.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded states data: {len(df)} rows")
    return df


def load_case_time_series(filepath=None):
    """Load India daily time series data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "case_time_series.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded case time series: {len(df)} rows")
    return df


def load_state_wise_daily(filepath=None):
    """Load state-wise daily data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "state_wise_daily.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded state-wise daily: {len(df)} rows")
    return df


def load_state_wise(filepath=None):
    """Load state-wise cumulative data."""
    if filepath is None:
        project_root = Path(__file__).parent.parent
        filepath = project_root / "data" / "state_wise.csv"
    
    df = pd.read_csv(filepath)
    print(f"Loaded state-wise cumulative: {len(df)} rows")
    return df


def clean_states_data(df):
    """Clean state-wise time series data."""
    df_clean = df.copy()
    
    # Remove total rows if present
    if 'State' in df_clean.columns:
        df_clean = df_clean[~df_clean['State'].str.contains('Total|India', case=False, na=False)]
    
    # Fill missing values
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    
    # Convert date column
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
    
    print(f"Cleaned: {len(df_clean)} rows")
    return df_clean


def get_state_column(df):
    """Find the state column name."""
    if df is None:
        return None
    for col in df.columns:
        if 'state' in col.lower():
            return col
    return df.columns[0]


def get_latest_by_state(df, date_col='Date', state_col=None):
    """Get latest record for each state."""
    if state_col is None:
        state_col = get_state_column(df)
    
    if date_col in df.columns:
        latest = df.loc[df.groupby(state_col)[date_col].idxmax()]
    else:
        latest = df.drop_duplicates(subset=[state_col], keep='last')
    
    return latest


def calculate_mortality_rate(df, deaths_col='Deceased', cases_col='Confirmed'):
    """Calculate mortality rate."""
    df_calc = df.copy()
    df_calc['Mortality_Rate'] = (df_calc[deaths_col] / df_calc[cases_col]) * 100
    df_calc['Mortality_Rate'] = df_calc['Mortality_Rate'].replace([np.inf, -np.inf], np.nan).fillna(0)
    return df_calc


def calculate_recovery_rate(df, recovered_col='Recovered', cases_col='Confirmed'):
    """Calculate recovery rate."""
    df_calc = df.copy()
    df_calc['Recovery_Rate'] = (df_calc[recovered_col] / df_calc[cases_col]) * 100
    df_calc['Recovery_Rate'] = df_calc['Recovery_Rate'].replace([np.inf, -np.inf], np.nan).fillna(0)
    return df_calc


def get_daily_stats(df, date_col='Date'):
    """Get daily statistics."""
    if date_col not in df.columns:
        return None
    
    daily = df.groupby(date_col).agg({
        'Confirmed': 'sum',
        'Deceased': 'sum',
        'Recovered': 'sum'
    }).reset_index()
    
    return daily


def export_for_tableau(states_df, daily_df, state_wise_df, output_dir=None):
    """Export data for Tableau."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "tableau"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    if states_df is not None:
        states_df.to_csv(output_dir / "states_tableau.csv", index=False)
    
    if daily_df is not None:
        daily_df.to_csv(output_dir / "daily_tableau.csv", index=False)
    
    if state_wise_df is not None:
        state_wise_df.to_csv(output_dir / "state_wise_tableau.csv", index=False)
    
    print(f"Exported to {output_dir}")


if __name__ == "__main__":
    states = load_states_data()
    states_clean = clean_states_data(states)
    
    print(f"\nCleaned data shape: {states_clean.shape}")
    print(f"Columns: {states_clean.columns.tolist()}")
