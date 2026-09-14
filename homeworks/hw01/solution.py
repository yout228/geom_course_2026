from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl as px
import data_utils as du


ROOT = Path(__file__).resolve().parents[2]
wells = ROOT / "data" / "raw" / "hw01" / "wells.csv"
layers = ROOT / "data" / "raw" / "hw01" / "layers.xlsx"
pumping_test = ROOT / "data" / "raw" / "hw01" / "pumping_test.txt"

coord = du.read_wells(wells)
lay = du.read_layers(layers)
pump = du.read_pumping_test(pumping_test)
du.info(coord)
du.info(lay)
du.info(pump)
print(coord.isna().sum())
wells_clean = coord.dropna(subset=["pressure_mpa"]).copy()
assert (wells_clean["radius_m"] > 0).all()
assert (lay["thickness_m"] > 0).all()
assert lay["porosity_fraction"].between(0, 1).all()

pressure_pa = wells_clean["pressure_mpa"] * 1_000_000
pressure_difference_mpa = 12 - wells_clean["pressure_mpa"]
relative_change_percent = pressure_difference_mpa / 12 * 100
print(relative_change_percent)
du.rast(coord)
log_radius = np.log(coord["radius_m"])
decay = np.exp(-pump["time_h"] / 36)

print(du.toch(coord["pressure_mpa"]))

print(du.toch(coord["radius_m"]))
print(du.toch(lay["thickness_m"]))
print(du.toch(lay["porosity_fraction"]))

pressure = wells_clean["pressure_mpa"].to_numpy()
print(pressure[0],pressure[-1])
print(pressure[:3])
print(pressure[::2])
mask = pressure < pressure.mean()
selected = pressure[mask]
print(selected)

mask2 = (wells_clean["radius_m"]*np.cos(wells_clean["azimuth_deg"]*np.pi/180))**2 + (wells_clean["radius_m"]*np.sin(wells_clean["azimuth_deg"]*np.pi/180))**2 > 100
selected2 = wells_clean[mask2]
print(selected2)

pressure_matrix = pump[
    ["boundary_pressure_mpa", "well_pressure_mpa"]
].to_numpy()

print(pressure_matrix.ndim)  
print(pressure_matrix.shape)  
print(pressure_matrix.size)   
print(pressure_matrix.dtype)

experiment_1 = pressure_matrix
experiment_2 = pressure_matrix + 0.05

pressure_cube = np.stack([experiment_1, experiment_2], axis=0)

print(pressure_cube[0])

print(pressure_cube[1])

print(pressure_cube[0,0])

print(pressure_cube[:, :, 1])

pressure_transposed = pressure_matrix.T

flat = pressure_cube.reshape(-1)
restored = flat.reshape(pressure_cube.shape)

assert np.allclose(restored, pressure_cube)
np.save(ROOT/"data"/"processed"/"hw01"/"pressure_matrix.npy", pressure_matrix)
matrix_loaded = np.load(ROOT/"data"/"processed"/"hw01"/"pressure_matrix.npy")

np.savez(ROOT/"data"/"processed"/"hw01"/"pressure_cube.npz",pressure_cube)
cube_loaded = np.load(ROOT/"data"/"processed"/"hw01"/ "pressure_cube.npz")

table1 = du.DatasetInfo("wells",coord)
table2 = du.DatasetInfo("layers",lay)
table3 = du.DatasetInfo("pumping_test",pump)

wells_clean.to_excel(ROOT/"data"/"processed"/"hw01"/"wells_clean.csv")

wb = px.Workbook()

sheet = wb.active

sheet.title = "Лист1"

sheet['B1'] = "min"
sheet['C1'] = "max"
sheet['D1'] = "mean"


du.wrxl(sheet,"pressure_mpa",coord["pressure_mpa"],"2")

du.wrxl(sheet,"radius_m",coord["radius_m"],"3")
du.wrxl(sheet,"thickness_m",lay["thickness_m"],"4")
du.wrxl(sheet,"porosity_fraction",lay["porosity_fraction"],"5")
    
wb.save(str(ROOT)+r'/data/processed/hw01/table_summary.xlsx')

f = open(str(ROOT)+r"/exports/hw01/results.txt",'w')
du.zapis(f,coord["pressure_mpa"],table1)
du.zapis(f,lay["thickness_m"],table2)
du.zapis(f,pump["time_h"],table3)
f.close() 
