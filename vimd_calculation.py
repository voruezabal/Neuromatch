import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

#%% The following script calculates Vertically Integrated Moisture divergence from U, V and Q

# Load the dataset once (your variables are in the same file)

years_i = [1973,1978,1983] #begining years
years_f = [1979,1984, 1989] # ending years


pathq = ["./q_1970_1973.nc",
         "./q_1974_1978.nc",
         "./q_1979_1983.nc",
         "./q_1984_1988.nc"]

pathu = ["./u_1970_1973.nc",
         "./u_1974_1977.nc",
         "./u_1978_1981.nc",
         "./u_1982_1985.nc",
         "./u_1986_1989.nc"]

pathv = ["./v_1970_1973.nc",
         "./v_1974_1977.nc",
         "./v_1978_1981.nc",
         "./v_1982_1985.nc",
         "./v_1986_1989.nc"]

# Extract variables
q_i = xr.open_VIMDataset(pathq)["q"]
u_i = xr.open_VIMDataset(pathu)["u"]
v_i = xr.open_VIMDataset(pathv)["v"]

for i in range(3):

    q = q_i.sel(valid_time = (q_i["valid_time.year"] < years_f[i]) & (q_i["valid_time.year"] > years_i[i]) ) #check that each file has diffent time lapse
    u = u_i.sel(valid_time = (u_i["valid_time.year"] < years_f[i])& (u_i["valid_time.year"] > years_i[i]))
    v = v_i.sel(valid_time = (v_i["valid_time.year"] < years_f[i]) & (v_i["valid_time.year"] > years_i[i]))
    #%%
    # Reverse pressure levels if needed (assumes highest level is at the top)
    q = q.assign_coords(pressure_level=q["pressure_level"][::-1])
    u = u.assign_coords(pressure_level=u["pressure_level"][::-1])
    v = v.assign_coords(pressure_level=v["pressure_level"][::-1])
    pressure_levels = q["pressure_level"].values

    #%%
    # Calculate pressure differences (dp) between levels
    # Pressure levels are in hPa, so convert to Pa by multiplying by 100.
    dp = np.diff(pressure_levels * 100)  # Now in Pa
    dp = np.append(dp, dp[-1])  # Append last value to maintain shape

    # Create dp as an xarray DataArray and expand to match q's dimensions
    dp = xr.DataArray(dp, dims=["pressure_level"], coords={"pressure_level": q["pressure_level"]})
    dp = dp.expand_dims({"valid_time": q["valid_time"], "latitude": q["latitude"], "longitude": q["longitude"]})
    dp = dp.transpose("valid_time", "pressure_level", "latitude", "longitude")

    #%%
    # Calculate moisture fluxes (q_u and q_v)
    q_u = q * u.values
    q_v = q * v.values

    g = 9.81      # Gravity (m/s^2)
    R = 6371000   # Earth's radius (m)

    # Vertically integrate the moisture fluxes
    q_u_integrated = (q_u * dp).sum(dim="pressure_level") / g
    q_v_integrated = (q_v * dp).sum(dim="pressure_level") / g

    #%%
    # Option 1: Convert coordinates to radians for proper horizontal differentiation.
    # Create new coordinates for longitude and latitude in radians.
    u = u.assign_coords(
        lon_rad=np.deg2rad(u["longitude"]),
        lat_rad=np.deg2rad(u["latitude"])
    )

    v = v.assign_coords(
        lon_rad=np.deg2rad(v["longitude"]),
        lat_rad=np.deg2rad(v["latitude"])
    )
    # The integrated flux arrays don't inherit the new coordinates automatically.
    # Assign the new 'lon_rad' and 'lat_rad' coordinates to the integrated fields.
    q_u_integrated = q_u_integrated.assign_coords(lon_rad=u["lon_rad"], lat_rad=u["lat_rad"])
    q_v_integrated = q_v_integrated.assign_coords(lon_rad=v["lon_rad"], lat_rad=v["lat_rad"])

    # Differentiate with respect to the radian coordinates:
    # - For longitude, the physical distance is R*cos(latitude) per radian.
    # - For latitude, the distance is R per radian.
    q_u_diff_x = q_u_integrated.differentiate("lon_rad") / (R * np.cos(q_u_integrated.lat_rad))
    q_v_diff_y = q_v_integrated.differentiate("lat_rad") / R

    # Compute the moisture flux divergence (VIMD)
    VIMD = q_u_diff_x + q_v_diff_y

    ds = xr.Dataset(

        {"vimd": (("time", "latitude","longitude"), VIMD.values)},

        coords={

            "longitude": q["longitude"].values,

            "latitude": q["latitude"].values,

            "time": q["valid_time"].values,

        },

    )

    # Optionally, save the result (if you want to save the VIMD data)
    ds.to_netcdf(f"vimd_{years_i[i]}_{years_f[i]}.nc")

