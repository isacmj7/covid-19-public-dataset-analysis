"""
Visualizations for COVID-19 India analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']


def save_fig(fig, filename, output_dir=None):
    """Save figure."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "visualizations"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    fig.savefig(output_dir / filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_daily_trend(df, date_col='Date', value_col='Confirmed', title="Daily COVID-19 Cases", output_dir=None):
    """Plot daily trend."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    daily = df.groupby(date_col)[value_col].sum().reset_index()
    
    ax.plot(daily[date_col], daily[value_col], linewidth=2, color=COLORS[0])
    ax.fill_between(daily[date_col], daily[value_col], alpha=0.3, color=COLORS[0])
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cases', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_fig(fig, '01_daily_trend.png', output_dir)


def plot_top_states(df, value_col='Confirmed', state_col='State', title="Top 10 States", output_dir=None, filename='02_top_states.png'):
    """Plot top states bar chart."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    state_totals = df.groupby(state_col)[value_col].max().reset_index()
    top10 = state_totals.nlargest(10, value_col)
    
    bars = ax.barh(range(len(top10)), top10[value_col].values, color=COLORS[0])
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10[state_col].values, fontsize=11)
    ax.invert_yaxis()
    
    ax.set_xlabel('Number of Cases', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    for bar, val in zip(bars, top10[value_col].values):
        ax.text(val + val*0.01, bar.get_y() + bar.get_height()/2, f'{val:,.0f}', 
               va='center', fontsize=9)
    
    plt.tight_layout()
    save_fig(fig, filename, output_dir)


def plot_cases_deaths_recovered(df, date_col='Date', output_dir=None):
    """Plot cases, deaths, and recovered trend."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    daily = df.groupby(date_col).agg({
        'Confirmed': 'sum',
        'Deceased': 'sum',
        'Recovered': 'sum'
    }).reset_index()
    
    # Confirmed cases
    axes[0].plot(daily[date_col], daily['Confirmed'], color=COLORS[0], linewidth=2)
    axes[0].fill_between(daily[date_col], daily['Confirmed'], alpha=0.3, color=COLORS[0])
    axes[0].set_title('Confirmed Cases', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Date')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Deaths
    axes[1].plot(daily[date_col], daily['Deceased'], color=COLORS[1], linewidth=2)
    axes[1].fill_between(daily[date_col], daily['Deceased'], alpha=0.3, color=COLORS[1])
    axes[1].set_title('Deaths', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Date')
    axes[1].tick_params(axis='x', rotation=45)
    
    # Recovered
    axes[2].plot(daily[date_col], daily['Recovered'], color=COLORS[2], linewidth=2)
    axes[2].fill_between(daily[date_col], daily['Recovered'], alpha=0.3, color=COLORS[2])
    axes[2].set_title('Recovered', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Date')
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.suptitle('COVID-19 India: Cases, Deaths, and Recoveries', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '03_cases_deaths_recovered.png', output_dir)


def plot_mortality_recovery_rates(df, state_col='State', output_dir=None):
    """Plot mortality and recovery rates by state."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    state_data = df.groupby(state_col).agg({
        'Confirmed': 'max',
        'Deceased': 'max',
        'Recovered': 'max'
    }).reset_index()
    
    state_data['Mortality_Rate'] = (state_data['Deceased'] / state_data['Confirmed']) * 100
    state_data['Recovery_Rate'] = (state_data['Recovered'] / state_data['Confirmed']) * 100
    
    top10 = state_data.nlargest(10, 'Confirmed')
    
    # Mortality rate
    bars1 = axes[0].barh(range(len(top10)), top10['Mortality_Rate'].values, color=COLORS[1])
    axes[0].set_yticks(range(len(top10)))
    axes[0].set_yticklabels(top10[state_col].values)
    axes[0].invert_yaxis()
    axes[0].set_xlabel('Mortality Rate (%)')
    axes[0].set_title('Mortality Rate by State', fontweight='bold')
    
    for bar, val in zip(bars1, top10['Mortality_Rate'].values):
        axes[0].text(val + 0.05, bar.get_y() + bar.get_height()/2, f'{val:.2f}%', va='center', fontsize=9)
    
    # Recovery rate
    bars2 = axes[1].barh(range(len(top10)), top10['Recovery_Rate'].values, color=COLORS[2])
    axes[1].set_yticks(range(len(top10)))
    axes[1].set_yticklabels(top10[state_col].values)
    axes[1].invert_yaxis()
    axes[1].set_xlabel('Recovery Rate (%)')
    axes[1].set_title('Recovery Rate by State', fontweight='bold')
    
    for bar, val in zip(bars2, top10['Recovery_Rate'].values):
        axes[1].text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=9)
    
    plt.suptitle('Mortality and Recovery Rates (Top 10 States by Cases)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '04_mortality_recovery_rates.png', output_dir)


def plot_testing_by_state(df, state_col='State', output_dir=None):
    """Plot testing statistics by state."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    if 'TotalSamples' in df.columns:
        value_col = 'TotalSamples'
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        value_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    
    if value_col is None:
        return
    
    state_totals = df.groupby(state_col)[value_col].max().reset_index()
    top15 = state_totals.nlargest(15, value_col)
    
    colors = [COLORS[i % len(COLORS)] for i in range(len(top15))]
    bars = ax.barh(range(len(top15)), top15[value_col].values, color=colors)
    ax.set_yticks(range(len(top15)))
    ax.set_yticklabels(top15[state_col].values, fontsize=10)
    ax.invert_yaxis()
    
    ax.set_xlabel('Total Samples Tested', fontsize=12)
    ax.set_title('COVID-19 Testing by State (Top 15)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    save_fig(fig, '05_testing_by_state.png', output_dir)


def plot_vaccination_progress(df, state_col='State', output_dir=None):
    """Plot vaccination progress by state."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    if 'Total Doses Administered' in df.columns:
        value_col = 'Total Doses Administered'
    elif 'Total' in df.columns:
        value_col = 'Total'
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        value_col = numeric_cols[0] if len(numeric_cols) > 0 else None
    
    if value_col is None:
        return
    
    state_totals = df.groupby(state_col)[value_col].max().reset_index()
    top15 = state_totals.nlargest(15, value_col)
    
    colors = [COLORS[i % len(COLORS)] for i in range(len(top15))]
    bars = ax.barh(range(len(top15)), top15[value_col].values, color=colors)
    ax.set_yticks(range(len(top15)))
    ax.set_yticklabels(top15[state_col].values, fontsize=10)
    ax.invert_yaxis()
    
    ax.set_xlabel('Total Doses Administered', fontsize=12)
    ax.set_title('COVID-19 Vaccination Progress by State (Top 15)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    save_fig(fig, '06_vaccination_progress.png', output_dir)


def plot_state_comparison(df, state_col='State', output_dir=None):
    """Plot state comparison for cases and deaths."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    state_data = df.groupby(state_col).agg({
        'Confirmed': 'max',
        'Deceased': 'max'
    }).reset_index()
    
    top10_cases = state_data.nlargest(10, 'Confirmed')
    top10_deaths = state_data.nlargest(10, 'Deceased')
    
    # Top 10 by cases
    bars1 = axes[0].barh(range(len(top10_cases)), top10_cases['Confirmed'].values, color=COLORS[0])
    axes[0].set_yticks(range(len(top10_cases)))
    axes[0].set_yticklabels(top10_cases[state_col].values)
    axes[0].invert_yaxis()
    axes[0].set_xlabel('Number of Cases')
    axes[0].set_title('Top 10 States by Confirmed Cases', fontweight='bold')
    
    # Top 10 by deaths
    bars2 = axes[1].barh(range(len(top10_deaths)), top10_deaths['Deceased'].values, color=COLORS[1])
    axes[1].set_yticks(range(len(top10_deaths)))
    axes[1].set_yticklabels(top10_deaths[state_col].values)
    axes[1].invert_yaxis()
    axes[1].set_xlabel('Number of Deaths')
    axes[1].set_title('Top 10 States by Deaths', fontweight='bold')
    
    plt.suptitle('State-wise Comparison: Cases vs Deaths', fontsize=14, fontweight='bold')
    plt.tight_layout()
    save_fig(fig, '07_state_comparison.png', output_dir)


def create_all_visualizations(states_df, daily_df=None, output_dir=None):
    """Create all charts."""
    print("Creating visualizations...")
    
    if states_df is not None and 'Date' in states_df.columns:
        plot_daily_trend(states_df, output_dir=output_dir)
        plot_top_states(states_df, output_dir=output_dir)
        plot_cases_deaths_recovered(states_df, output_dir=output_dir)
        plot_mortality_recovery_rates(states_df, output_dir=output_dir)
        plot_state_comparison(states_df, output_dir=output_dir)
    
    print("Done!")


if __name__ == "__main__":
    from data_processing import load_states_data, clean_states_data
    
    states = load_states_data()
    states_clean = clean_states_data(states)
    
    create_all_visualizations(states_clean)
