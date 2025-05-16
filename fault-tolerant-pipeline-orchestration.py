from prefect import flow, task
from prefect_dask import DaskTaskRunner
from prefect.blocks.notifications import SlackWebhook

@task(retries=3, retry_delay=60)
def process_sector(sector):
    try:
        lc = download_sector(sector)
        return analyze_sector(lc)
    except MastError as e:
        raise Retry from e
        
@flow(task_runner=DaskTaskRunner())
def full_pipeline(tic_ids, sectors):
    config = load_config()
    notify = SlackWebhook.load("pipeline-alerts")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tic_id in tic_ids:
            for sector in sectors:
                futures.append(process_sector.submit(tic_id, sector))
                
        for future in as_completed(futures):
            try:
                result = future.result()
                generate_report(result)
            except Exception as e:
                notify(f"Failed processing {future}: {str(e)}")