from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


ROOT = Path(__file__).resolve().parents[2]

loaded = np.load(ROOT/"homeworks"/"hw04"/"field_data.npz",allow_pickle = True)

required_keys = {
    "time_h",
    "radius_m",
    "well_id",
    "pressure_field",
    "contour_levels",
}

available_keys = set(loaded.keys())

missing = required_keys - available_keys
extra   = available_keys - required_keys

if missing:
    raise KeyError(f"Отсутствуют обязательные ключи: {sorted(missing)}")

if extra:
    print(f"️ Обнаружены лишние ключи: {sorted(extra)}")



assert loaded["time_h"].shape == (13,)
assert loaded["radius_m"].shape == (7,)
assert loaded["well_id"].shape == (7,)
assert loaded["pressure_field"].shape == (13, 7)
assert loaded["contour_levels"].shape == (9,)
assert np.all(np.diff(loaded["time_h"]) > 0)
assert np.all(np.diff(loaded["radius_m"]) > 0)

assert (ROOT/"figures"/"hw04"/"pressure_maps.svg").exists()
assert (ROOT/"figures"/"hw04"/"pressure_maps.svg").stat().st_size > 0

time_grid, radius_grid = np.meshgrid(
    loaded["time_h"],
    loaded["radius_m"],
    indexing="ij",)

time_index, radius_index = np.indices(
   loaded["pressure_field"].shape)
well_names_long = loaded["well_id"][
    radius_index.reshape(-1)
]
dftable = pd.DataFrame({
    "time_h":   time_grid.reshape(-1),
    "radius_m": radius_grid.reshape(-1),
    "well_id":  well_names_long.reshape(-1),
    "pressure_mpa":loaded["pressure_field"].reshape(-1),
})


assert dftable.shape == (91, 4)
assert dftable["time_h"].nunique() == 13
assert dftable["radius_m"].nunique() == 7
assert not dftable.isna().any().any()

dftable.to_csv(ROOT/"homeworks"/"hw05"/"pressure_long.csv", index=False)

loaded2 = pd.read_csv(ROOT/"homeworks"/"hw05"/"pressure_long.csv")
assert loaded2.shape == (91, 4)
assert loaded2["time_h"].nunique() == 13
assert loaded2["radius_m"].nunique() == 7
assert not loaded2.isna().any().any()


fig, ax = plt.subplots(figsize=(6, 8),constrained_layout=True )

ax.set_xscale("log")
ax.set_xlabel("Расстояние, м")
ax.set_ylabel("Давление, МПа")



margin = 0.1
time_h = loaded["time_h"]
y_min = loaded["pressure_field"].min() - margin
y_max = loaded["pressure_field"].max() + margin
pod, = ax.plot(loaded["radius_m"], loaded["pressure_field"][0], marker="o", color="tab:blue")
ax.set_ylim(y_min, y_max)
title =ax.set_title(f"t = {time_h[0]:.2f} ч")
def update(frame_index):
    pod.set_data(loaded["radius_m"], loaded["pressure_field"][frame_index])  
    title.set_text(f"t = {time_h[frame_index]:.2f} ч")
    return pod, title      

gif =FuncAnimation(fig, update, frames=len(loaded["time_h"]))
gif.save(ROOT/"figures"/"hw05"/"pressure_animation.gif",writer=PillowWriter(fps=1))
plt.close(fig)

print("Done!")
