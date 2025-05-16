# After EB model subtraction
residuals = eb_model.compute_residuals()

# Initialize analyzer with original time axis
analyzer = ResidualAnalyzer(
    time=lc.time.value,
    residuals=residuals,
    flux_err=lc.flux_err.value,
    period_eb=period_guess.value
)

# Run TLS with EB-masked data
mask = analyzer.mask_eb_regions()
results = analyzer.run_tls(period_min=0.5)

# Plot TLS results
plt.figure()
plt.plot(results.periods, results.power, 'k-')
plt.xlabel('Period (days)')
plt.ylabel('TLS Power')
plt.axvline(results.period, color='r', ls='--')
plt.show()

# Vetting candidates
if results.snr > 7 and results.depth > 0:
    vetter = CandidateVetter(
        time=lc.time.value[mask],
        flux=residuals[mask],
        candidate_period=results.period,
        epoch=results.T0
    )
    odd_even_diff = vetter.odd_even_test()
    if odd_even_diff < 3*np.std(residuals):
        print(f"Potential candidate at {results.period:.2f} days!")