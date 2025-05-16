import numpy as np
from scipy.optimize import curve_fit
import ellc
import matplotlib.pyplot as plt

class BinaryStarModel:
    def __init__(self, time, flux, flux_err, period, t0):
        """
        Initialize with preprocessed light curve data
        :param time: Phase-folded time array
        :param flux: Normalized flux array
        :param flux_err: Flux errors
        :param period: Orbital period (days)
        :param t0: Reference epoch (BJD/TDB)
        """
        self.time = time
        self.flux = flux
        self.flux_err = flux_err
        self.period = period
        self.t0 = t0
        self.params = {}  # To store best-fit parameters

    def eb_model(self, time, q, r_1, r_2, sbratio, incl, f_s, f_c):
        """
        Basic EB model using ellc
        :param q: Mass ratio (m2/m1)
        :param r_1: Primary radius [a]
        :param r_2: Secondary radius [a]
        :param sbratio: Surface brightness ratio
        :param incl: Inclination (degrees)
        :param f_s: Spot parameters
        :param f_c: Spot parameters
        """
        return ellc.lc(
            time_obs=time,
            radius_1=r_1,
            radius_2=r_2,
            sbratio=sbratio,
            incl=incl,
            q=q,
            ld_1='quad',
            ld_2='quad',
            ldc_1=[0.5, 0.5],  # Initial limb-darkening coeffs
            ldc_2=[0.5, 0.5],
            shape_1='sphere',
            shape_2='sphere',
            spots_1=f_s,
            spots_2=f_c,
            t_zero=self.t0,
            period=self.period,
        )

    def fit_model(self, initial_guess=None):
        """Fit the EB model to data using curve_fit"""
        if initial_guess is None:
            # Default initial parameter guesses
            initial_guess = [
                0.5,    # q
                0.1,    # r_1
                0.1,    # r_2
                0.2,    # sbratio
                85.0,   # incl
                0.0,    # f_s
                0.0     # f_c
            ]

        bounds = (
            [0.01, 0.01, 0.01, 0.01, 70, -1, -1],  # Lower bounds
            [1.0, 0.5, 0.5, 1.0, 90, 1, 1]          # Upper bounds
        )

        popt, pcov = curve_fit(
            self.eb_model,
            self.time,
            self.flux,
            p0=initial_guess,
            sigma=self.flux_err,
            bounds=bounds
        )

        self.params = {
            'q': popt[0],
            'r_1': popt[1],
            'r_2': popt[2],
            'sbratio': popt[3],
            'incl': popt[4],
            'f_s': popt[5],
            'f_c': popt[6]
        }
        return popt, pcov

    def plot_model(self):
        """Plot data vs best-fit model"""
        model_flux = self.eb_model(self.time, **self.params)
        
        plt.figure(figsize=(10,6))
        plt.errorbar(self.time, self.flux, self.flux_err, 
                    fmt='.k', alpha=0.3, label='Data')
        plt.plot(np.sort(self.time), 
                model_flux[np.argsort(self.time)], 
                'r-', label='Model')
        plt.xlabel('Phase')
        plt.ylabel('Normalized Flux')
        plt.legend()
        plt.show()

    def compute_residuals(self):
        """Calculate residuals after model subtraction"""
        model_flux = self.eb_model(self.time, **self.params)
        return self.flux - model_flux