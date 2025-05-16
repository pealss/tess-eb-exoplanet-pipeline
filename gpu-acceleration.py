searcher = AcceleratedTransitSearch(time, residuals, err)
results = searcher.run()  # Automatically uses GPU if available