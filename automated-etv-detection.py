class ETVAnalyzer:
    def __init__(self, time, flux, period_eb, t0):
        self.time = time
        self.flux = flux
        self.period = period_eb
        self.t0 = t0
        
    def find_eclipse_times(self, method='template'):
        """Detect eclipse timings using cross-correlation"""
        # Create phase-folded template
        phase = (self.time - self.t0) % self.period / self.period
        sorted_idx = np.argsort(phase)
        template = np.interp(phase, phase[sorted_idx], self.flux[sorted_idx])
        
        # Cross-correlate with original light curve
        corr = signal.correlate(self.flux - np.mean(self.flux), 
                              template - np.mean(template), 
                              mode='same')
        
        # Find eclipse peaks
        peaks, _ = signal.find_peaks(corr, height=np.std(corr), 
                                distance=int(0.1*self.period*24*60))  # 10% period separation
        return self.time[peaks]

    def calculate_etvs(self, eclipse_times):
        """Compute O-C diagram with linear ephemeris"""
        cycle_numbers = np.round((eclipse_times - self.t0) / self.period)
        predicted_times = self.t0 + cycle_numbers * self.period
        return eclipse_times - predicted_times

    def fit_etv_model(self, oc_times, max_terms=3):
        """Fit polynomial + sinusoid ETV model"""
        t = oc_times - oc_times.mean()
        design_matrix = np.vstack([t**n for n in range(1, max_terms+1)]).T
        coeffs = np.linalg.lstsq(design_matrix, oc_times, rcond=None)[0]
        return coeffs