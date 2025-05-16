from astropy.timeseries import BoxLeastSquares
from transitleastsquares import transitleastsquares  # TLS (pip install transitleastsquares)
import astropy.units as u

class ResidualAnalyzer:
    def __init__(self, time, residuals, flux_err, period_eb):
        """
        :param time: Original time array (not phase-folded)
        :param residuals: Flux residuals after EB subtraction
        :param flux_err: Original flux errors
        :param period_eb: EB orbital period (for transit search masking)
        """
        self.time = time
        self.residuals = residuals
        self.flux_err = flux_err
        self.period_eb = period_eb
        
    def run_bls(self, duration_grid=None):
        """Box Least Squares periodogram implementation"""
        if duration_grid is None:
            duration_grid = np.linspace(0.01, 0.3, 15)  # Days
            
        bls = BoxLeastSquares(self.time, self.residuals, self.flux_err)
        bls_power = bls.power(period=period_grid, 
                             duration=duration_grid,
                             objective='snr')
        
        return bls_power

    def run_tls(self, period_min=0.5, period_max=None):
        """Transit Least Squares implementation (more sensitive to small planets)"""
        if period_max is None:
            period_max = self.period_eb/2  # Avoid EB harmonics
            
        model = transitleastsquares(self.time, self.residuals, self.flux_err)
        results = model.power(period_min=period_min, 
                            period_max=period_max,
                            show_progress_bar=False)
        return results

    def mask_eb_regions(self, phase_buffer=0.1):
        """Mask EB eclipses in residual data"""
        phased_time = (self.time - self.time[0]) % self.period_eb
        in_eclipse = np.where((phased_time < phase_buffer) | 
                            (phased_time > (1-phase_buffer))[0]
        mask = np.ones_like(self.time, dtype=bool)
        mask[in_eclipse] = False
        return mask

    def find_etvs(self, eclipse_times, max_order=3):
        """Eclipse Timing Variations analysis"""
        # eclipse_times = [list of primary/secondary eclipse times]
        O_C = eclipse_times - (eclipse_times[0] + 
                             np.arange(len(eclipse_times)) * self.period_eb)
        
        # Fit polynomial to O-C diagram
        coeffs = np.polyfit(np.arange(len(O_C)), O_C, max_order)
        return {'O_C': O_C, 'poly_coeffs': coeffs}

class CandidateVetter:
    def __init__(self, time, flux, candidate_period, epoch):
        self.time = time
        self.flux = flux
        self.period = candidate_period
        self.epoch = epoch
        
    def odd_even_test(self):
        """Check for depth consistency between odd/even transits"""
        even_transits = self.flux[((self.time - self.epoch)/self.period % 2) < 1]
        odd_transits = self.flux[((self.time - self.epoch)/self.period % 2) >= 1]
        return np.abs(np.median(even_transits) - np.median(odd_transits))

    def centroid_test(self, window=0.2):
        """Check for out-of-transit centroid shifts"""
        # Implementation requires full-frame images
        pass