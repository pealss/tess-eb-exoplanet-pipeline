# Assuming you have folded_lc from previous steps
time = folded_lc.phase.value
flux = folded_lc.flux.value
flux_err = folded_lc.flux_err.value

# Initialize model with period from preprocessing
eb_model = BinaryStarModel(
    time=time,
    flux=flux,
    flux_err=flux_err,
    period=period_guess.value,  # From LightCurveProcessor
    t0=lc.time[0].value        # Initial epoch
)

# Fit with initial guesses
initial_params = [0.6, 0.15, 0.12, 0.3, 87, 0.0, 0.0]
best_fit_params, cov = eb_model.fit_model(initial_params)

# Visualize
eb_model.plot_model()

# Get residuals for later analysis
residuals = eb_model.compute_residuals()