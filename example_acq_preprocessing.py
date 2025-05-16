# Data Acquisition
tic_id = "123456789"  # Example TIC ID from TESS EBs catalog
data_handler = TessDataHandler(tic_id=tic_id)
lcs = data_handler.download_lcs(sector=25)

# Preprocessing
lc = lcs[0].PDCSAP_FLUX  # Use PDCSAP flux
processor = LightCurveProcessor(lc)
processor.remove_outliers(sigma=3)
processor.normalize()
processor.detrend_sff()

# Get initial period estimate
period_guess = processor.find_initial_period()
folded_lc = processor.phase_fold(period=period_guess, 
                                epoch_time=lc.time[0])

# Visualization
folded_lc.scatter()