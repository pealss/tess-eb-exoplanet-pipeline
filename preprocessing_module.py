from scipy import signal
from lightkurve.correctors import SFFCorrector

class LightCurveProcessor:
    def __init__(self, lc):
        self.lc = lc
        self.clean_lc = None
        self.norm_lc = None
        self.detrended_lc = None
        
    def remove_outliers(self, sigma=5):
        """Sigma-clipping outlier removal"""
        self.clean_lc = self.lc.remove_outliers(sigma=sigma)
        return self.clean_lc
    
    def normalize(self):
        """Normalize light curve"""
        self.norm_lc = self.clean_lc.normalize()
        return self.norm_lc
    
    def detrend_sff(self, polyorder=5):
        """Systematic Error Correction using SFF"""
        sff = SFFCorrector()
        self.detrended_lc = sff.correct(self.norm_lc, polyorder=polyorder)
        return self.detrended_lc
    
    def phase_fold(self, period, epoch_time):
        """Phase folding with given period and epoch"""
        folded_lc = self.detrended_lc.fold(period=period, epoch_time=epoch_time)
        return folded_lc

    def find_initial_period(self):
        """Automated period finding using Lomb-Scargle"""
        pg = self.detrended_lc.to_periodogram(method='lombscargle')
        return pg.period_at_max_power