try:
    from cuvarbase.bls import BLS
    GPU_ENABLED = True
except ImportError:
    from astropy.timeseries import BoxLeastSquares
    GPU_ENABLED = False

class AcceleratedTransitSearch:
    def __init__(self, time, flux, flux_err):
        self.time = np.ascontiguousarray(time, dtype=np.float64)
        self.flux = np.ascontiguousarray(flux, dtype=np.float64)
        self.flux_err = np.ascontiguousarray(flux_err, dtype=np.float64)
        
    def _gpu_bls(self, duration_grid=(0.1, 0.3, 50), freq_grid=1e-3):
        bls = BLS()
        results = bls.autopower(self.time, self.flux, self.flux_err,
                              duration_grid=duration_grid,
                              freq_min=freq_grid,
                              freq_max=1/0.5)  # 0.5 day minimum period
        return results

    def _cpu_bls(self, duration_grid=np.linspace(0.1, 0.3, 50)):
        model = BoxLeastSquares(self.time, self.flux, self.flux_err)
        periods = 1 / np.linspace(1e-3, 2, 10000)
        return model.power(periods, duration_grid)

    def run(self):
        if GPU_ENABLED:
            return self._gpu_bls()
        else:
            return self._cpu_bls()