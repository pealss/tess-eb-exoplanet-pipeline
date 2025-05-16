from pipeline import TessDataHandler, LightCurveProcessor, BinaryStarModel, ResidualAnalyzer

def main(tic_id, sectors):
    # Data Acquisition
    handler = TessDataHandler(tic_id=tic_id)
    lcs = handler.download_lcs(sector=sectors)
    
    # Preprocessing
    processor = LightCurveProcessor(lcs[0].PDCSAP_FLUX)
    processor.remove_outliers(sigma=3)
    processor.normalize()
    detrended_lc = processor.detrend_sff()
    
    # EB Modeling
    period = processor.find_initial_period()
    folded_lc = processor.phase_fold(period, lcs[0].time[0].value)
    model = BinaryStarModel(folded_lc.phase, folded_lc.flux, folded_lc.flux_err, period, lcs[0].time[0].value)
    best_params, _ = model.fit_model()
    
    # Residual Analysis
    residuals = model.compute_residuals()
    analyzer = ResidualAnalyzer(lcs[0].time.value, residuals, folded_lc.flux_err, period)
    tls_results = analyzer.run_tls()
    
    # Generate Report
    generate_full_report(best_params, tls_results, "results/final_report.pdf")

if __name__ == "__main__":
    main(tic_id="123456789", sectors=[25, 26])