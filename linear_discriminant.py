#%%
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from matplotlib.colors import ListedColormap

#The following script read csv files and use its information to make a 3D linear discriminant and plot it in 2D

PATH_H ="/path/" #list of input files from tornado, rain and hail data
PATHR ="/path/"
PATHT ="/path/"

OUT ="/path/"

## Files provided cape, vimd, shear, mixed ratio and lapse rate infomation. Keep the fist 3 and delete the rest. Some conditions are requested

hail = pd.read_csv(PATHH)
rain = pd.read_csv(PATHR)
tornado = pd.read_csv(PATHT)

hail = hail.drop(columns=['mr',"LR"])
hail = hail.loc[(hail["CAPE"] > 500) & (hail["Cort"] > 10)]

rain = rain.drop(columns=['mr',"LR"])
rain = rain.loc[(rain["CAPE"] > 0) & (rain["Cort"] > 0)]

tornado = tornado.drop(columns=['mr',"LR"])
tornado = tornado.loc[(tornado["CAPE"] > 500) & (tornado["Cort"] > 10)]


# Sample data (replace with your actual data)
X1 = pd.concat([hail, tornado,rain])#, control] ignore_index=True)
#%%


X1["CAPE"] = np.log10(X1["CAPE"])
X1["Cort"] = np.log10(X1["Cort"])
X1["mvimd"] = np.log10(X1["mvimd"]*-10000)

X = np.array(X1)[:,-3:]
y = [0]*len(hail) + [0]*len(tornado) + [1]*len(rain) # 0 is severe class, 1 is rain class

#
target_names = ["Severe", "Rain"]
#%%

# Create an LDA model
lda = LinearDiscriminantAnalysis(solver ="svd")

# Fit the model to the data
lda.fit(X, y)

# Make predictions
predictions = lda.predict(X)

# Calculate the accuracy (you can use other metrics as well)
accuracy = np.mean(predictions == y)
print(f"Accuracy: {accuracy}")

X_r2 = lda.fit_transform(X, y=y)

h = len(hail) + len(tornado)+ len(tornado_2)
r= len(rain) + h



plt.rcParams['font.size'] = 14

# Adjust figure size to 174mm x 234mm, as asked by some scientific journals

fig, ax = plt.subplots(figsize=(150 / 25.4, 120/ 25.4))  # Convert mm to inches

ax.scatter(X[h:r, 0], X_r2[h:r], color="b", label='Non Severe', alpha=0.7)
ax.scatter(X[0:h, 0], X_r2[0:h], color="r", label='Severe', alpha=0.7)
# ax.scatter(X_r2[h:r,0], X_r2[h:r,1], label='Rain', alpha=0.7)

ax.set_xlabel('LDA Component 1')
ax.set_ylabel('LDA Component 2')
ax.legend()

# Save figure before showing
fig.savefig( f'{OUT}disc_severos.png', dpi=300, bbox_inches='tight')

# Get and print figure size in mm
fig_width, fig_height = fig.get_size_inches()
fig_width_mm = fig_width * 25.4
fig_height_mm = fig_height * 25.4

print(f"Figure size: {fig_width_mm:.2f} mm × {fig_height_mm:.2f} mm")

plt.show()  # Now show the figure


#%%

