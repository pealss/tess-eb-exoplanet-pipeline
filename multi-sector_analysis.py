class MultiSectorAnalyzer:
    def __init__(self, tic_id):
        self.tic_id = tic_id
        self.sectors = []
        self.residuals = []
        self.models = []
        
    def combine_sectors(self):
        """Stitch light curves from multiple sectors"""
        search_result = lk.search_lightcurve(f"TIC {self.tic_id}", mission='TESS')
        self.all_lcs = search_result.download_all()
        self.stiched_lc = self.all_lcs.stitch()
        return self.stiched_lc
    
    def sector_by_sector_analysis(self):
        """Run pipeline on individual sectors"""
        results = []
        for lc in self.all_lcs:
            # Run full pipeline on each sector
            processor = LightCurveProcessor(lc)
            # ... previous processing steps ...
            model = BinaryStarModel(...)
            residuals = model.compute_residuals()
            results.append({'sector': lc.sector, 
                          'residuals': residuals,
                          'model_params': model.params})
        return results

    def combined_period_search(self):
        """Search for periodic signals in combined residuals"""
        all_residuals = np.concatenate([r['residuals'] for r in self.results])
        return AcceleratedTransitSearch(self.stiched_lc.time, all_residuals).run()