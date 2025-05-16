etv_analyzer = ETVAnalyzer(time, flux, period, t0)
eclipse_times = etv_analyzer.find_eclipse_times()
oc = etv_analyzer.calculate_etvs(eclipse_times)
etv_coeffs = etv_analyzer.fit_etv_model(oc)