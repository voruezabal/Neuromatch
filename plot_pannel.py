#%%
import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np 
import cartopy.crs as ccrs	# Graficar mapas 
import cartopy.feature 	# Notacion de punto (escribir todo)
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# The following script plots a pannel of 8 maps from different time stamps

PATH ="/path/"
SALIDAS = "/path/"

a = xr.open_dataset(PATH)["cape"]

#%%
hour = ["00:00","03:00","06:00","09:00","12:00","15:00","18:00","21:00"]

fig, axx = plt.subplots(nrows = 2, ncols = 4, figsize = (20,9),
            subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
#gs = gridspec.GridSpec(4,4) 
ax = axx.flatten()
fig.subplots_adjust(hspace=0, wspace = 0)
lons, lats = np.meshgrid(a['lon'], a['lat'])
#%%
for cont in range(0,8,1):

    gl = ax[cont].gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
    linewidth=2, color='gray', alpha=0.5, linestyle='--')
    if (cont != 0) & (cont != 4) :
        gl.left_labels = False
    else:  gl.left_labels = True
    if (cont != 3) & (cont != 7) :
        gl.right_labels = False 
    else:  gl.right_labels = True
    gl.top_labels = False
                #gl.ylabels_left = False
    gl.xlines = False
    if (cont == 0) | (cont == 1) | (cont == 2) | (cont == 3)  :
        gl.bottom_labels = False
                #
                # gl.xlocator = mticker.FixedLocator([-74,-40, -33])
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()

    gl.xlabel_style = {'fontsize': 15,'color': 'black'}

    gl.ylabel_style = {'fontsize': 15,'color': 'black'}
                            
    crs_latlon = ccrs.PlateCarree()
    brks = np.arange(0,100,10)

    im=ax[cont].contourf(lons, lats, a[cont,:,:],
    levels = brks,cmap = "turbo", 
    transform = ccrs.PlateCarree(),zorder = -20)

    ax[cont].add_feature(cartopy.feature.COASTLINE)
    ax[cont].add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5)
                            
    states_provinces = cartopy.feature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='10m',
            facecolor='none')
                            
    ax[cont].add_feature(states_provinces, edgecolor='black')
                            
    ax[cont].set_title("hora " + hour[cont],fontsize = 20)   
cbar_ax = fig.add_axes([0.3, 0.05, 0.4, 0.02])
cbar = fig.colorbar(
im, 
cax=cbar_ax, 
orientation = 'horizontal', 
shrink = 0.65, pad = 0.035, aspect = 40
)
cbar.set_label('°C', fontsize = 16)
cbar.set_ticks(brks)
cbar.ax.tick_params(labelsize=12, length = 5, width = 1)
cbar.outline.set_linewidth(1)        

fig.suptitle("Title " + str(hour[cont]) ,fontsize=30,y=0.93)

fig.savefig(SALIDAS + 'plot_pannel.png', dpi=300, bbox_inches='tight')
# %%
