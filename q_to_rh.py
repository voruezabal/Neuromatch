#%%
import numpy as np
import xarray as xr
import dask.array as da

#%%
def specific_humidity_to_relative_humidity(specific_humidity, temperature, pressure):
    epsilon_1 = 1 / 0.622
    a1 = 611.21
    a3_w = 17.502
    a3_i = 22.587
    a4_w = 32.19
    a4_i = -0.7
    T0 = 273.16
    Tice = 250.16

    # Vectorized computation for e_sat using Dask-friendly expressions
    e_sat_i = a1 * np.exp(a3_i * (temperature - T0) / (temperature - a4_i))
    e_sat_w = a1 * np.exp(a3_w * (temperature - T0) / (temperature - a4_w))
    
    # Alpha as a vectorized array for efficiency
    alpha = xr.where(temperature < Tice, 0, xr.where(temperature < T0, ((temperature - Tice) / (T0 - Tice)) ** 2, 1))
    e_sat = alpha * e_sat_w + (1 - alpha) * e_sat_i

    # Calculate RH directly
    RH = (pressure * specific_humidity * epsilon_1) / (e_sat * (1 + specific_humidity * (epsilon_1 - 1))) * 100
    return RH

#%%
inicio = list(range(1970, 2005, 3))
fin = list(range(1972, 2006, 3)) 
for i, j in zip(inicio, fin):

    filen = f"./ta_NCC_{i}_{j}.nc"
    gph = "./orog_NorEsm1_rotated.nc"
    hr= f"./hus_NCC_{i}_{j}.nc"
    OUT = "/path/"

    # Load datasets as dask arrays for lazy evaluation and slice 
    q = xr.open_dataset(hr)["ta"]
    q= q.sel(latitude = slice(-45,-10), longitude = slice(-75,-30))
    t = xr.open_dataset(filen)["ta"]
    t = t.sel(latitude = slice(-45,-10), longitude = slice(-75,-30))

    # Convert pressure levels to the same shape as the arrays, leveraging broadcasting
    opres = q["level"] * 100
    op = opres.broadcast_like(q)
    #%%
    # Apply the function using xarray's apply_ufunc with dask parallelization
    new_rh = specific_humidity_to_relative_humidity(q,t,op)


    # Rename the output and save it
    new_rh = new_rh.rename("hr")
    new_rh.to_netcdf(f"{OUT}rh_{i}_{j}_NCC.nc")

#%%
