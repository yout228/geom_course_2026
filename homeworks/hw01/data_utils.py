from pathlib import Path
import pandas as pd
import numpy as np
import openpyxl as px


def read_wells(path):
    return pd.read_csv(path)
def read_layers(path):
    return pd.read_excel(path)

def read_pumping_test(path):
    return pd.read_csv(path, sep="\t")

def info(table):
    print(table.shape)      
    print(table.columns)     
    print(table.dtypes)      
    print(table.head())      

def rast(coord):
    theta_rad = coord["azimuth_deg"]*np.pi/180
    x_check = coord["radius_m"]*np.cos(theta_rad)
    y_check = coord["radius_m"]*np.sin(theta_rad)
    print(np.allclose(x_check,coord["x_m"],atol = 0.02))
    print(np.allclose(y_check,coord["y_m"],atol = 0.02))


def toch(table):
    return np.amin(table),np.amax(table),np.mean(table)

class DatasetInfo:
    def __init__(self, name, table):
        self.name = name
        self.rows, self.columns = table.shape

    def describe(self):
        return f"{self.name}: {self.rows} строк, {self.columns} столбцов"

def wrxl(sheet,name,table,ex):
    t = "BCD"
    sheet["A"+str(ex)] = name
    a = toch(table)
    for i in range(2,5):
        sheet[t[i-2]+ex] = a[i-2]


def zapis(file,table,Data):
    a = toch(table)
    file.write(Data.describe() +f" min: {a[0]}, max: {a[1]}, mean: {a[2]}" +'\n')
 
