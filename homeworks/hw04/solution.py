from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

loaded = np.load(ROOT/"homeworks"/"hw03"/"viz_data.npz",allow_pickle = True)

required_keys = {
    "time_h",
    "boundary_pressure_mpa",
    "well_pressure_mpa",
    "pressure_drop_mpa",
    "well_id",
    "radius_m",
    "observation_pressure_mpa",
    "observation_drop_mpa",
}
available_keys = set(loaded.keys())

missing = required_keys - available_keys
extra   = available_keys - required_keys

if missing:
    raise KeyError(f"Отсутствуют обязательные ключи: {sorted(missing)}")

if extra:
    print(f"️ Обнаружены лишние ключи: {sorted(extra)}")

print("Все обязательные ключи на месте")

assert loaded["time_h"].shape == (13,)
assert loaded["well_pressure_mpa"].shape == (13,)
assert loaded["well_id"].shape == (7,)
assert loaded["radius_m"].shape == (7,)
assert loaded["observation_pressure_mpa"].shape == (7,)
assert np.all(np.diff(loaded["time_h"]) > 0)
assert np.all(np.diff(loaded["radius_m"]) > 0)

time_component = loaded["well_pressure_mpa"] - loaded["well_pressure_mpa"][0]
radius_component = (loaded["observation_pressure_mpa"]
    - loaded["observation_pressure_mpa"][0])

pressure_field = (loaded["well_pressure_mpa"][0]
    + time_component[:, np.newaxis]
    + radius_component[np.newaxis, :]
)

assert pressure_field.shape == (13, 7)


field_for_plot = pressure_field.T
assert field_for_plot.shape == (7, 13)

vmin = pressure_field.min()
vmax = pressure_field.max()
levels = np.linspace(vmin, vmax, 9)

fig, axes = plt.subplots(1, 2,figsize=(12, 8),constrained_layout=True )

mesh = axes[0].pcolormesh(
    loaded["time_h"],
    loaded["radius_m"],
    field_for_plot,
    shading="auto",
    cmap="viridis",
    vmin=vmin,
    vmax=vmax,
)

assert (loaded["radius_m"] > 0).all()
axes[0].set_yscale("log")

axes[0].set_ylabel("Расстояние, м")
axes[0].set_xlabel("Время, ч")
axes[0].set_title("A — тепловая карта по ячейкам")
fig.colorbar(mesh, ax=axes[0], label="Давление, МПа")

filled = axes[1].contourf(
    loaded["time_h"],
    loaded["radius_m"],
    field_for_plot,
    levels=levels,
    cmap="viridis",
    vmin=vmin,
    vmax=vmax,
)
axes[1].set_yscale("log")

axes[1].set_ylabel("Расстояние, м")
axes[1].set_xlabel("Время, ч")
axes[1].set_title("B — заливка по уровням с изолиниями")
fig.colorbar(filled, ax=axes[1], label="Давление, МПа")

lines = axes[1].contour(
    loaded["time_h"],
    loaded["radius_m"],
    field_for_plot,
    levels=levels,
    colors="black",
    linewidths=0.6,
)
axes[1].clabel(lines, fmt="%.2f")

fig.savefig(ROOT/"figures"/"hw04"/ "pressure_maps.png", dpi=200)
fig.savefig(ROOT/"figures"/"hw04"/ "pressure_maps.svg")
plt.close(fig)

fig2,ax = plt.subplots(figsize=(6, 8),constrained_layout=True )
lines2 = ax.contour(
    loaded["time_h"],
    loaded["radius_m"],
    field_for_plot,
    levels=levels,
    colors="black",
    linewidths=0.6,
)
ax.clabel(lines2, fmt="%.2f")
ax.set_ylabel("Расстояние, м")
ax.set_xlabel("Время, ч")
ax.set_title("Только изолинии")

fig2.savefig(ROOT/"figures"/"hw04"/ "pressure_isolines.png", dpi=200)
fig2.savefig(ROOT/"figures"/"hw04"/ "pressure_isolines.svg")

np.savez(
    ROOT/"homeworks"/"hw04"/"field_data.npz",
    time_h=loaded["time_h"],
    radius_m=loaded["radius_m"],
    well_id=loaded["well_id"],
    pressure_field=pressure_field,
    contour_levels=levels,
)

loaded2 = np.load(ROOT/"homeworks"/"hw04"/"field_data.npz",allow_pickle = True)
assert np.allclose(loaded2["time_h"],loaded["time_h"])
assert loaded2["pressure_field"].shape == (13, 7)

print("Done!")
