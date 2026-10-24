from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
wells_path = ROOT / "data" / "processed" / "hw01" / "wells_clean.csv"
pumping_path = ROOT / "data" / "raw" / "hw01" / "pumping_test.txt"
required_figures = [ROOT/"figures"/"hw02"/"pressure_over_time.svg",ROOT/"figures"/"hw02"/"pressure_by_radius.svg"]

for path in required_figures:
    assert path.exists()
    assert path.stat().st_size > 0
pumping_test = pd.read_csv(pumping_path, sep="\t")
wells = pd.read_csv(wells_path)

assert pumping_test.shape == (13, 4)
assert wells.shape[0] == 7
assert not pumping_test.isna().any().any()
assert not wells.isna().any().any()

time_h = pumping_test["time_h"].to_numpy()
boundary_pressure_mpa = pumping_test["boundary_pressure_mpa"].to_numpy()
well_pressure_mpa = pumping_test["well_pressure_mpa"].to_numpy()
well_id = wells["well_id"].to_numpy()
radius_m = wells["radius_m"].to_numpy()
observation_pressure_mpa = wells["pressure_mpa"].to_numpy()
order = np.argsort(radius_m)
well_id = well_id[order]
radius_m = radius_m[order]
observation_pressure_mpa = observation_pressure_mpa[order]
pressure_drop_mpa = boundary_pressure_mpa - well_pressure_mpa
observation_drop_mpa = 12.0 - observation_pressure_mpa

fig, ax = plt.subplots(2,2,figsize=(12, 8),constrained_layout=True,)

ax[0,0].plot(time_h,boundary_pressure_mpa,'g',label='давление на границе')
ax[0,0].plot(time_h,well_pressure_mpa,'r',label='давление в скважине')
ax[0,0].legend()
ax[0,0].set_xlabel('Время, ч', fontsize=12)
ax[0,0].set_ylabel('Давление, МПа', fontsize=12)
ax[0,0].set_title("A: Давление во времени")

cs = ax[0, 1].scatter(radius_m, observation_pressure_mpa,c=observation_pressure_mpa, cmap="viridis")
cb = ax[0, 1].figure.colorbar(cs, ax=ax[0, 1] ,orientation='vertical',location='left')
cb.set_ticks([])
ax[0,1].set_xlabel('Расстояние, м', fontsize=12)
cb.set_label('Давление, МПа', fontsize=12)
cb.ax.yaxis.set_label_position('left')
ax[0,1].set_title("B: Давление в наблюдательных скважинах")

ax[1,0].bar(well_id,observation_drop_mpa)
ax[1,0].set_xlabel('ID скважины', fontsize=12)
ax[1,0].set_ylabel('Давление, МПа', fontsize=12)
ax[1,0].set_title("C: Давления по скважинам")

ax[1,1].boxplot([boundary_pressure_mpa,well_pressure_mpa],tick_labels=['давление на границе', 'давление на скважине'])
ax[1,1].set_ylabel('Давление на скважине, МПа', fontsize=12)
ax[1,1].set_title("D: Размах давления")



fig2,ax2 = plt.subplots(1,2,figsize=(12, 8),constrained_layout=True,)

ax2[0].boxplot([boundary_pressure_mpa,well_pressure_mpa],tick_labels=['давление на границе', 'давление на скважине'])
ax2[0].set_ylabel('Давление,МПа', fontsize=12)
ax2[0].set_title("A: Ящик с усами")

ax2[1].violinplot([boundary_pressure_mpa,well_pressure_mpa])
ax2[1].set_ylabel('Давление , МПа', fontsize=12)
ax2[1].set_xticks([1, 2])
ax2[1].set_xticklabels(['Давление на границе', 'Давление на скважине'])
ax2[1].set_title("B: Скрипичная диаграмма")

 

#fig.show()
#fig2.show()

fig.savefig(ROOT /"figures"/"hw03"/"pressure_overview.png", dpi=200, bbox_inches="tight")
fig.savefig(ROOT /"figures"/"hw03"/"pressure_overview.svg" , bbox_inches="tight")

fig2.savefig(ROOT /"figures"/"hw03"/"distributions.png", dpi=200, bbox_inches="tight")
fig2.savefig(ROOT /"figures"/"hw03"/"distributions.svg" , bbox_inches="tight")

plt.close(fig)
plt.close(fig2)


np.savez(ROOT/"homeworks"/"hw03"/"viz_data.npz",time_h=time_h,
    boundary_pressure_mpa=boundary_pressure_mpa,
    well_pressure_mpa=well_pressure_mpa,
    pressure_drop_mpa=pressure_drop_mpa,
    well_id=well_id,
    radius_m=radius_m,
    observation_pressure_mpa=observation_pressure_mpa,
    observation_drop_mpa=observation_drop_mpa)

loaded = np.load(ROOT/"homeworks"/"hw03"/"viz_data.npz",allow_pickle = True)
assert np.allclose(loaded["time_h"],time_h)
assert loaded["well_id"].shape == well_id.shape

print("Done!")
