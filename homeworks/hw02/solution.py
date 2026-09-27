import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl as px
import plot_utils as pu

ROOT = Path(__file__).resolve().parents[2]
pump = ROOT / "data" / "raw" / "hw01" / "pumping_test.txt"
wells = ROOT/ "data"/ "processed"/ "hw01" / "wells_clean.csv"
fig_dir = ROOT/ "figures/hw02"
fig_dir.mkdir(parents= True,exist_ok = True)
pumping_test = pd.read_csv(pump, sep="\t")
wells_clean = pd.read_csv(wells, sep=",")
pu.plot_pressure_over_time(pumping_test,fig_dir)
wells_sorted = wells_clean.sort_values(by ="radius_m")
assert (wells_sorted["radius_m"] > 0).all()
pu.plot_pressure_by_radius(wells_sorted, fig_dir)

assert (fig_dir / "pressure_over_time.png").exists()
assert (fig_dir / "pressure_over_time.svg").exists()
assert (fig_dir / "pressure_by_radius.png").exists()
assert (fig_dir / "pressure_by_radius.svg").exists()

print("Done!")
