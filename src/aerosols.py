import pyrcel as pm


class aerosols(object):
    def __init__(self, name, ds, gammas, n_total, ks, sigmas, is_binned=False):
        self.name = name
        self.ds = ds
        self.rs = [0.5 * d for d in ds]
        self.ks = ks
        self.gammas = gammas
        self.n_totals = [n_total for d in ds]
        self.sigmas = sigmas
        self.is_binned = is_binned

        self.n_modes = len(ds)
        self.ns = [self.get_individual_ns(n_total, gamma) for n_total, gamma in zip(self.n_totals, self.gammas)]
        self.pyr_dist = self.get_pyrcel_distribution()

    @staticmethod
    def get_individual_ns(n_total, gamma):
        return n_total * gamma

    def get_pyrcel_distribution(self, bins=50):
        dists = [None] * self.n_modes

        for i in range(self.n_modes):
            if self.is_binned:
                dists[i] = pm.AerosolSpecies((self.name + str(i)),
                                            pm.Lognorm(mu=self.rs[i], sigma=self.sigmas[i], N=self.ns[i]),
                                            kappa=self.ks[i], bins= int(bins/self.n_modes))
            else:
                dists[i] = pm.AerosolSpecies((self.name + str(i)),
                                            pm.Lognorm(mu=self.rs[i], sigma=self.sigmas[i], N=self.ns[i]),
                                            kappa=self.ks[i], bins=bins)

        return dists


size_distribution = {
    "bgd":
        {"ds": [0.05, 0.15, 0.4 ],
         "gammas": [0.9, 0.15, 0.05],
         "ks": [0.88, 1.28, 1.28],
         "sigmas": [1.6, 1.6, 1.6]
         },
    "pol": {"ds": [0.09],
            "gammas": [1.0],
            "ks": [0.88],
            "sigmas": [1.6]
            }
}