#%%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
#%%
PATH = "/path/"
OUT = "/path/"

#%% The following scripts take the months from september to february from a era 5 Netcdf and make a boxplot of a specific region

ds = xr.open_dataset(PATH)["mvimd"]

ds = ds.sel(time = (ds["time.month"] > 8) |  (ds["time.month"] < 3))


#%%
region = ["East","west"]

for AREA in range(1,2,1):

    if AREA == 0:

        LATMAX = -22
        LATMIN = -38
        LONMIN = -62
        LONMAX = -55



    elif AREA == 1:
        LATMAX = -25
        LATMIN = -37
        LONMIN = -70
        LONMAX = -63



    box_max = ds1.sel(latitude=slice(LATMAX, LATMIN), longitude=slice(LONMIN,LONMAX))
    max = box_max.values.ravel()

    fig1, ax1 = plt.subplots(figsize=(4, 4))
    # Customizing the boxplot
    # Customizing the boxplot without outliers (fliers)
    ax1.set_title("MVIMFD", fontsize=12, fontweight='bold',y=1, x = 0.05)
    ax1.boxplot(max[~np.isnan(max)]] , #take non nan values
            labels=["values"], 
            whis=(5,95),
            patch_artist=True,  # Fill the boxes with color
            boxprops=dict(facecolor='steelblue', color='darkblue'),
            medianprops=dict(color='white', linewidth=2),
            whiskerprops=dict(color='darkblue', linewidth=1.5),
            capprops=dict(color='darkblue', linewidth=1.5),
            showfliers=False,  # Suppress the outliers (dots)
            widths=0.3) 

    # Add grid lines and set better Y-axis limits
    ax1.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax1.set_ylabel("MVIMFD kg/m**2*s", fontsize=12,rotation = 90,labelpad = 10)

    # Save the plot
    plt.show()
    fig1.savefig(f'{OUT}Id_boxplot_MVIMFD_extremes_{region[AREA]}.png', dpi=300, bbox_inches='tight')

#%%
