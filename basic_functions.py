import xarray as xr
import numpy as np

#%% funciones
def TLCL ( tk, rh ):
    zeroRK = 0
    oneRK = 1

    term1 = 1.0 / ( tk - 55.0 )

    if ( rh > zeroRK ):
      term2 = ( np.log(rh/100.0)  / 2840.0 )
    else:
      term2 = ( np.log(0.001/oneRK) / 2840.0 )

    denom = term1 - term2

    tlcl = ( oneRK / denom ) + 55*oneRK

    return tlcl

def theta_e ( tK, p, rh, mixr ):
    
     R  = 287.04         # Universal gas constant (J/deg kg)
     lv = 2.54*(10**6)   # Latent heat of vaporization
     Cp = 1004.67        # Specific heat of dry air constant
     p00 = 1000


     tlc = TLCL ( tK, rh )

     thetae = (tK * (p00/p)**( (R/Cp)*(1.- ( (.28E-3)*mixr*1000.) ) ) )* \
        np.exp( (((3.376/tlc)-.00254))*mixr*1000.*(1.+(.81E-3)*mixr*1000.)) 
  
     return thetae

def saturation_mixing_ratio ( tK, p ):
    
    es = 6.122 * np.exp( (17.67*(tK-273.15))/ (tK-29.66) )
    ws = ( 0.622*es ) / ( (p/100.0)-es )
    
    return ws

def theta ( t, p ):
  Rd =  287.04
  Cp = 1004.67
  p00 = 1000
  theta = t * ( (p00/p)**(Rd/Cp) )
  
  return theta

def virtual_temperature( tK, w ): 
  
  Tv = tK * ( 1.0 + (w/0.622) ) / ( 1.0 + w )

  return Tv

import math


def the2T(thetaeK, pres, flag):
    # Constants
    R = 287.04  # Dry gas constant (J/(kg·K))
    Cp = 1004.67  # Specific heat for dry air (J/(kg·K))
    Kappa = R / Cp
    Lv = 2.500E+6  # Latent heat of vaporization at 0 deg. C (J/kg)
    
    # Initial guess for temperature of the parcel
    tovtheta = (pres / 100000.0) ** (R / Cp)
    tparcel = thetaeK / math.exp(Lv * 0.012 / (Cp * 295.0)) * tovtheta

    iter = 1
    found = False
    flag = False

    while True:
        if iter > 105:
            break

        tguess_2 = tparcel + 1.0

        svpr = 6.122 * math.exp((17.67 * (tparcel - 273.15)) / (tparcel - 29.66))
        smixr = (0.622 * svpr) / ((pres / 100.0) - svpr)
        svpr2 = 6.122 * math.exp((17.67 * (tguess_2 - 273.15)) / (tguess_2 - 29.66))
        smixr2 = (0.622 * svpr2) / ((pres / 100.0) - svpr2)

        thetae_check = theta_e(tparcel, pres / 100.0,100, smixr)
        thetae_check2 = theta_e(tguess_2, pres / 100.0,100, smixr2)

        if abs(thetaeK - thetae_check) < 0.001:
            found = True
            flag = True
            break

        correction = (thetaeK - thetae_check) / (thetae_check2 - thetae_check)
        tparcel += correction

        iter += 1

    if not found:
        print("Warning! Thetae to temperature calculation did not converge!")
        print("Thetae:", thetaeK, "Pressure:", pres)

    return tparcel


# %%
