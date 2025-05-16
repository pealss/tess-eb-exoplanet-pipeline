from pipeline import TessEBPipeline

# Initialize with AI components
pipeline = TessEBPipeline(
    use_ai=True,
    enable_3d=True,
    notification_level="slack"
)

# Process multiple targets
results = pipeline.batch_process(
    tic_ids=["TIC 123456", "TIC 789012"],
    sectors=[25, 26],
    output_dir="results"
)

# Generate consolidated report
pipeline.generate_master_report(
    output_file="final_report.pdf",
    include=[
        'system_parameters',
        'candidate_planets',
        'spectral_analysis'
    ]
)