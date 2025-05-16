from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner

@task(retries=3, retry_delay_seconds=10)
def data_acquisition(tic_id):
    # Implementation using previous TessDataHandler
    pass

@task
def preprocessing(raw_lc):
    # Implementation using LightCurveProcessor
    pass

@flow(task_runner=SequentialTaskRunner())
def main_pipeline(tic_id, sector=None):
    logger = get_run_logger()
    try:
        lc = data_acquisition(tic_id)
        processed = preprocessing(lc)
        model_params = eb_modeling(processed)
        residuals = residual_analysis(processed, model_params)
        candidates = planet_search(residuals)
        generate_full_report(model_params, candidates)
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise