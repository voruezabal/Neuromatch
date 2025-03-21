#%%
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
#%%
PATH = "/home/victoria.oruezabal/datoscirrus/qxv_1989_2020.nc"
SALIDAS = "/home/victoria.oruezabal/salidas/ciclos_series_paper/"
#%%
ds = xr.open_dataset(PATH)["mvimd"]

ds = ds.sel(time = (ds["time.month"] > 8) |  (ds["time.month"] < 3))

ds1 = ds.sel(time=ds["time.year"].isin([1997, 2006, 2011, 2012, 2013, 2017]))
ds2 = ds.sel(time=ds["time.year"].isin([2004,2009,2010,2016]))

#%%
region = ["este","oeste"]

for AREA in range(1,2,1):

    if AREA == 0:

        LATMAX = -22
        LATMIN = -38
        LONMIN = -62
        LONMAX = -55

        ds1 = ds.sel(time=ds["time.year"].isin([1997, 2006, 2011, 2012, 2013, 2017]))
        ds2 = ds.sel(time=ds["time.year"].isin([2004,2009,2010,2016]))

    elif AREA == 1:
        LATMAX = -25
        LATMIN = -37
        LONMIN = -70
        LONMAX = -63

        ds1 = ds.sel(time=ds["time.year"].isin([1992, 1994, 1997, 2006]))
        ds2 = ds.sel(time=ds["time.year"].isin([2009,2019]))

    box_mayores = ds1.sel(latitude=slice(LATMAX, LATMIN), longitude=slice(LONMIN,LONMAX))
    box_menores = ds2.sel(latitude=slice(LATMAX, LATMIN), longitude=slice(LONMIN,LONMAX))
    #box_mayores = box_mayores.where(box_mayores < -0.010  )
    #box_menores = box_menores.where(box_menores < -0.010 )

    mayores = box_mayores.values.ravel()
    menores = box_menores.values.ravel()
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    # Customizing the boxplot
    # Customizing the boxplot without outliers (fliers)
    ax1.set_title("MVIMFD", fontsize=12, fontweight='bold',y=1, x = 0.05)
    ax1.boxplot([mayores[~np.isnan(mayores)],menores[~np.isnan(menores)]] , #[mayores, menores],
            labels=["Years highly Severe","Years minimally severe"], 
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
    fig1.savefig(f'{SALIDAS}Id_boxplot_MVIMFD_extremes_{region[AREA]}.png', dpi=300, bbox_inches='tight')

#%%