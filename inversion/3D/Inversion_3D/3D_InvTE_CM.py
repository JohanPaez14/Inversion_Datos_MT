from SimPEG import (
    maps, utils, data, optimization, maps, regularization, 
    inverse_problem, directives, inversion, data_misfit
)
import discretize
from discretize.utils import mkvc, refine_tree_xyz
from SimPEG.electromagnetics import natural_source as nsem
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from pymatsolver import Solver
from matplotlib.colors import LogNorm
from ipywidgets import interact, widgets
import warnings
from mtpy import MT, MTCollection

from pathlib import Path

import pandas as pd
from discretize import TensorMesh
from discretize.utils import active_from_xyz
from SimPEG.utils import mkvc, model_builder
from SimPEG import maps
from scipy.interpolate import Rbf

# -----------------> CARGAR DATOS
print("Reading Data: MT Data")
interp_periods = np.logspace(np.log10(0.0032), np.log10(9.2), 20)
file_path_sdf = Path(__file__).parent / "data"/ "sdf_20.pkl"
file_path_gdf = Path(__file__).parent / "data"/ "gdf_20.pkl"
sdf = pd.read_pickle(file_path_sdf)
gdf = pd.read_pickle(file_path_gdf)
rx_loc = np.hstack(
    (mkvc(gdf.model_east.to_numpy(), 2), 
     mkvc(gdf.model_north.to_numpy(), 2),
     mkvc(gdf.model_elevation.to_numpy(),2))
     )
long_X = rx_loc[:,0].max()-rx_loc[:,0].min()
long_Y = rx_loc[:,1].max()-rx_loc[:,1].min()
long_Z_TM = 2879+3000

print("Reading Data: TE Interpolation")
arrayTE = np.load(Path(__file__).parent / "data" / "TE_15.npy")
array_TE = np.pad( arrayTE, pad_width=((2, 2), (2, 2), (2, 0)), mode='constant', constant_values=50               )
res_data_TM = array_TE.flatten(order="F")

#----------------------------> TE
#-------> MALLA
print("Creating Mesh")
def make_example_mesh():
    hx = [(long_X/15,2,-1),(long_X/15, 15.0),(long_X/15,2,1)]
    hy = [(long_Y/15,2,-1),(long_Y/15, 15.0),(long_Y/15,2,1)]
    hz = [(long_Z_TM/15, 15.0),(long_Z_TM/15,2,1)]
    origin = ["C","C",-3000]
    meshTE = TensorMesh([hx, hy, hz], origin)
    return meshTE

meshTE = make_example_mesh()
halfspace_value = 50.0
[xx, yy] = np.meshgrid(meshTE.nodes_x, meshTE.nodes_y)
rbf = Rbf(rx_loc[:,0], rx_loc[:,1], rx_loc[:,2], function='linear', epsilon=2)
zz = rbf(xx.flatten(), yy.flatten())
zz = zz.reshape(xx.shape)
topo = np.c_[mkvc(xx), mkvc(yy), mkvc (zz)]
air_value = 0.0
ind_active = active_from_xyz(meshTE, topo, "CC")
model_map = maps.InjectActiveCells(meshTE, ind_active, air_value)
model = halfspace_value * np.ones(ind_active.sum())
dataTE_active = ind_active*res_data_TM
dataTE_active[dataTE_active == 0.0] = 1e-8
halfspace_value = np.ones(meshTE.nC) * 1e-8
halfspace_value[ind_active] = 50.0

#-------> INVERSION
print("Doing List of Orientations Impedance")
rx_list = []
rx_orientations_impedance = ['xx', 'xy', 'yx', 'yy']
for rx_orientation in rx_orientations_impedance:    
    rx_list.append(     
        nsem.receivers.PointNaturalSource(
            rx_loc, orientation=rx_orientation, component="real"
        )
    )
    rx_list.append(
        nsem.receivers.PointNaturalSource(
            rx_loc, orientation=rx_orientation, component="imag"
        )
    )
rx_orientations_tipper = ['zx', 'zy']
for rx_orientation in rx_orientations_tipper:    
    rx_list.append(     
        nsem.receivers.Point3DTipper(
            rx_loc, orientation=rx_orientation, component="real"
        )
    )
    rx_list.append(
        nsem.receivers.Point3DTipper(
            rx_loc, orientation=rx_orientation, component="imag"
        )
    )
src_list = [nsem.sources.PlanewaveXYPrimary(rx_list, frequency=f) for f in 1./interp_periods]
survey = nsem.Survey(src_list)
rx_orientations = rx_orientations_impedance + rx_orientations_tipper

print("Doing List of Data Obs")
frequencies = 1/interp_periods
components = ["zxx", "zxy", "zyx", "zyy", "tzx", "tzy"]
n_rx = rx_loc.shape[0]
n_freq = len(interp_periods)
n_component = 2
n_orientation = len(rx_orientations)

f_dict = dict([(round(ff, 5), ii) for ii, ff in enumerate(1/interp_periods)])
observations = np.zeros((n_freq, n_orientation, n_component, n_rx))
errors = np.zeros_like(observations)
for s_index, station in enumerate(gdf.station):
    station_df = sdf.loc[sdf.station == station]
    station_df.set_index("period", inplace=True)
    for row in station_df.itertuples():
        f_index = f_dict[round(1./row.Index, 5)]
        for c_index, comp in enumerate(components):
            value = getattr(row, comp)
            err = getattr(row, f"{comp}_model_error")
            observations[f_index, c_index, 0, s_index] = value.real
            observations[f_index, c_index, 1, s_index] = value.imag
            errors[f_index, c_index, 0, s_index] = err
            errors[f_index, c_index, 1, s_index] = err
        
observations[np.where(observations == 0)] = 100
errors[np.where(errors == 0)] = np.inf 
data_object = data.Data(survey, dobs=observations.flatten(), standard_deviation=errors.flatten())

print("Creating Simulation")
active_map = maps.InjectActiveCells(
    mesh=meshTE, indActive=ind_active, valInactive=np.log(1e-8)
)
mapping = maps.ExpMap(meshTE) * active_map
simulation = nsem.simulation.Simulation3DPrimarySecondary(
    meshTE,
    survey=survey,
    sigmaMap=mapping,
    sigmaPrimary=halfspace_value,
    solver=Solver
)

print("Doing Inversion")
import time
start = time.time()

opt = optimization.ProjectedGNCG(maxIter=40, maxIterCG=20, upper=np.inf, lower=-np.inf)
opt.remember('xc')
dmis = data_misfit.L2DataMisfit(data=data_object, simulation=simulation)
dz = meshTE.h[2].min()
dx = meshTE.h[0].min()
regmap = maps.IdentityMap(nP=int(ind_active.sum()))
reg = regularization.Sparse(meshTE, indActive=ind_active, mapping=regmap)
reg.alpha_s = 1e-6
reg.alpha_x = dz/dx
reg.alpha_y = dz/dx
reg.alpha_z = 1.
inv_prob = inverse_problem.BaseInvProblem(dmis, reg, opt)
beta = directives.BetaSchedule(coolingRate=1, coolingFactor=3)
beta_est = directives.BetaEstimate_ByEig(beta0_ratio=1e0)
target = directives.TargetMisfit()
save_dictionary = directives.SaveOutputDictEveryIteration()
directive_list = [beta, beta_est, target, save_dictionary]
inv = inversion.BaseInversion(inv_prob, directiveList=directive_list)
m_0 = np.log(dataTE_active[ind_active])
mopt = inv.run(m_0)
end = time.time()
print('total time:', end-start)

print("Exporting Data Inversion")
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_dir, "output", "Inversion_TE.pkl")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
import pickle
out_dict = save_dictionary.outDict 
with open(output_path, "wb") as file:
    pickle.dump(out_dict, file)
