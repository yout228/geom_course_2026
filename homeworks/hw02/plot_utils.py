import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path



def plot_pressure_over_time(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True, alpha=0.3)
    ax.plot(table["time_h"], table["boundary_pressure_mpa"], color='gray',marker='o' , linewidth=2, label='давление на границе')
    ax.plot(table["time_h"], table["well_pressure_mpa"], color='crimson', marker='*', linewidth=2.5, label='давление в скважине')
    ax.set_title('Изменение давления во времени', fontsize=14, fontweight='bold')
    ax.set_xlabel('Время, ч', fontsize=12)
    ax.set_ylabel('Давление, МПа', fontsize=12)
    min_index = table["well_pressure_mpa"].idxmin()
    min_time = table.loc[min_index, "time_h"]
    min_pressure = table.loc[min_index, "well_pressure_mpa"]
    ax.annotate("min = "+str(round(min_pressure,2)), xy=(min_time, min_pressure),xytext=(min_time-25,min_pressure+0.5),arrowprops=dict(facecolor='gray', shrink=0.05))
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir/"pressure_over_time.png", dpi=200, bbox_inches="tight")
    fig.savefig(output_dir/"pressure_over_time.svg", bbox_inches="tight")
    #plt.show()
    plt.close(fig)
    


def plot_pressure_by_radius(table, output_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.grid(True,alpha=0.3)
    ax.set_xscale("log")
    ax.plot(table["radius_m"], table["pressure_mpa"], color='teal',marker='s',linestyle="none")
    ax.set_title('Давление в наблюдательных скважинах', fontsize=14, fontweight='bold')
    ax.set_xlabel('Расстояние, м', fontsize=12)
    ax.set_ylabel('Давление, МПа', fontsize=12)
    fig.tight_layout()
    fig.savefig(output_dir / 'pressure_by_radius.png', dpi=200, bbox_inches="tight")
    fig.savefig(output_dir / 'pressure_by_radius.svg', bbox_inches="tight")
    #plt.show()
    plt.close(fig)

