import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def lognormal(N_0: float, S: float, d_m: float, d: float):
    r_m = d_m * 0.5
    r = d * 0.5
    return (N_0 / (np.sqrt(2 * np.pi) * np.log(S))) * np.exp(-(np.log(r / r_m) ** 2) / (2 * np.log(S) ** 2))


def fitness(N: float, N_min: float, N_max: float, dd: float):
    if N < N_min:
        return 0
    if N > N_max:
        return 0
    return dd*N


acruise_ship = "../data/acruise_dists/Ship.csv"

print("Started")
ship_dist = pd.read_csv(acruise_ship)

ship_dist = ship_dist.loc[ship_dist['x']>0.03]

d_bin_mean_ship = np.log(ship_dist['x'] * 1e-6).diff().mean()

ship_dist['mean'] = 1e4 - ship_dist['mean']

ship_dist['error'] = np.abs((1e4 - ship_dist['error']) - ship_dist['mean'])

ship_dist['max'] = ship_dist['mean'] + ship_dist['error']
ship_dist['min'] = ship_dist['mean'] - ship_dist['error']


ship_dist['N_obs'] = ship_dist['mean'] * d_bin_mean_ship

ship_dist['N_obs_max'] = ship_dist['max'] * d_bin_mean_ship

ship_dist['N_obs_min'] = ship_dist['min'] * d_bin_mean_ship

n_iter = 30
dms = np.logspace(np.log10(0.03), np.log10(0.3), n_iter)
ss = np.linspace(1.1, 2, n_iter)
n0s = np.linspace(20, 2000, n_iter)

DMS, SS, NOS = np.meshgrid(dms, ss, n0s)

F_ship = np.zeros([n_iter, n_iter, n_iter])

F_ship_max = 0.9

F_ship_min = 0.9

i_ship, j_ship, k_ship = (0, 0, 0)

uncertain_indexes_ship = []
certain_indexes_ship =[]

for i, dm in enumerate(dms):
    for j, s in enumerate(ss):
        for k, n0 in enumerate(n0s):
            ship_dist['N_an'] = 1e-6 * ship_dist.apply(
                lambda x: lognormal(N_0=NOS[i, j, k] * 1e6, S=SS[i, j, k], d_m=1e-6 * DMS[i, j, k], d=1e-6 * x['x']),
                axis=1)
            ship_dist['dF'] = ship_dist.apply(
                lambda x: fitness(N=x['N_an'], N_min=x['N_obs_min'], N_max=x['N_obs_max'], dd=d_bin_mean_ship), axis=1)
            ship_dist['dN'] = ship_dist.apply(lambda x: d_bin_mean_ship*x['N_an'], axis=1)
            F_ship[i, j, k] = ship_dist['dF'].sum()
            F_ship[i, j, k] = ship_dist['dF'].sum() /ship_dist['dN'].sum()

            if F_ship[i, j, k] > F_ship_max:
                i_ship, j_ship, k_ship = (i, j, k)
                F_ship_max = F_ship[i, j, k]

            if F_ship[i, j, k] < F_ship_min:
                uncertain_indexes_ship.append([i, j, k])
            else:
                certain_indexes_ship.append([i, j, k])


ship_dist['N_an'] = 1e-6 * ship_dist.apply(
    lambda x: lognormal(N_0=1e6 * NOS[i_ship, j_ship, k_ship], S=SS[i_ship, j_ship, k_ship],
                        d_m=1e-6 * DMS[i_ship, j_ship, k_ship], d=1e-6 * x['x']), axis=1)

print(f"Ship: {NOS[i_ship, j_ship, k_ship], DMS[i_ship, j_ship, k_ship], SS[i_ship, j_ship, k_ship], F_ship[i_ship, j_ship, k_ship]}")

n0_certain_ship = []
dm_certain_ship = []
s_certain_ship = []



for index in certain_indexes_ship:
    i,j,k = index
    n0_certain_ship.append(NOS[i, j, k])
    dm_certain_ship.append(DMS[i, j, k])
    s_certain_ship.append(SS[i, j, k])


print(f"Ship")
print(f"N: [{np.quantile(n0_certain_ship, 0.1)}, {np.quantile(n0_certain_ship, 0.9)}]")
print(f"dm: [{np.quantile(dm_certain_ship, 0.1)}, {np.quantile(dm_certain_ship, 0.9)}]")
print(f"S: [{np.quantile(s_certain_ship, 0.1)}, {np.quantile(s_certain_ship, 0.9)}]")

plt.figure()
plt.semilogx(ship_dist['x'], ship_dist['N_obs'], 'r--', label= 'Mean')
plt.fill_between(ship_dist['x'], ship_dist['N_obs_min'], ship_dist['N_obs_max'], alpha=0.2, color='r', label ='Uncertainty region' )
plt.semilogx(ship_dist['x'], ship_dist['N_an'], 'r', label= 'Example')

plt.xlabel(r"d [$\mu$m]")
plt.ylabel(r"N [cm$^{-3}$]")
plt.legend()
plt.xlim([0.02, 3])

paper_figures_dir = '/Users/rodrigoribeiro/Documents/Imperial_PhD/Papers/MeterologicalControlsUndetectedTracks/figures/'
plt.savefig(paper_figures_dir + 'uncertainty_dist.pdf', dpi=300)