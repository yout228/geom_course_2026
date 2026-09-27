import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl as px

def plot_pressure_over_time(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()


    ax.plot(table["time_h"], table["boundary_pressure_mpa"], color='gray',marker='o' , linewidth=2, label='давление на границе')
    ax.plot(table["time_h"], table["well_pressure_mpa"], color='crimson', marker='*', linewidth=2.5, label='давление в скважине')
    ax.legend()
    ax.set_title('Изменение давления во времени', fontsize=14, fontweight='bold')
    ax.set_xlabel('Время, ч', fontsize=12)
    ax.set_ylabel('Давление, МПа', fontsize=12)
    min_index = table["well_pressure_mpa"].idxmin()
    min_time = table.loc[min_index, "time_h"]
    min_pressure = table.loc[min_index, "well_pressure_mpa"]
    ax.annotate(round(min_pressure,2), xy=(min_time, min_pressure), xytext=(min_time, round(min_pressure,2)),arrowprops=dict(facecolor='black', shrink=0.05))
    fig.savefig(output_dir / 'pressure_over_time.png', dpi=200, bbox_inches="tight")
    fig.savefig(output_dir / 'pressure_over_time.svg', bbox_inches="tight")
    #plt.show()
    plt.close(fig)
    


def plot_pressure_by_radius(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True,alpha=0.3)
    fig.tight_layout()
    ax.set_xscale("log")
    ax.plot(table["radius_m"], table["pressure_mpa"], color='teal',marker='s',linestyle="none", label='давление на границе')
    ax.legend()
    ax.set_title('Давление в наблюдательных скважинах', fontsize=14, fontweight='bold')
    ax.set_xlabel('Расстояние, м', fontsize=12)
    ax.set_ylabel('Давление, МПа', fontsize=12)
    fig.savefig(output_dir / 'pressure_by_radius.png', dpi=200, bbox_inches="tight")
    fig.savefig(output_dir / 'pressure_by_radius.svg', bbox_inches="tight")

    #plt.show()
    plt.close(fig)

