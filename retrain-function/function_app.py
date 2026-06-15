import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient

from model import train_and_save

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 0 1 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def daily_retrain(myTimer: func.TimerRequest) -> None:

    if myTimer.past_due:
        logging.warning("Timer is past due — running now.")

    logging.info("Starting daily gold model retraining...")

    try:
        train_and_save()
    except Exception as e:
        logging.error(f"Training failed: {e}")
        raise

    connection_string = os.environ.get("BLOB_CONNECTION_STRING")
    if not connection_string:
        logging.error("BLOB_CONNECTION_STRING not set. Skipping upload.")
        return

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container = "models"

    files = [
        "gold_model.keras",
        "gold_scaler.pkl",
        "gold_metrics.pkl",
        "gold_data.pkl"
    ]

    for file_name in files:
        if not os.path.exists(file_name):
            logging.warning(f"{file_name} not found, skipping.")
            continue
        try:
            blob_client = blob_service_client.get_blob_client(
                container=container,
                blob=file_name
            )
            with open(file_name, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Uploaded {file_name} to blob storage.")
        except Exception as e:
            logging.error(f"Failed to upload {file_name}: {e}")

    logging.info("Daily retraining completed successfully.")