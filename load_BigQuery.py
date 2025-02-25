import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
import os

# reassign env variables.
os.environ["CREDENTIALS__CLIENT_EMAIL"] = os.environ.get("GOOGLE_CLIENT_EMAIL")
os.environ["CREDENTIALS__PRIVATE_KEY"] = os.environ.get("GOOGLE_PRIVATE_KEY").replace("\\n", "\n")
os.environ["CREDENTIALS__PROJECT_ID"] = os.environ.get("GOOGLE_PROJECT_ID")

@dlt.resource(name="rides", write_disposition="replace")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page

pipeline = dlt.pipeline(
    pipeline_name='taxi_data',
    destination='duckdb', # <--- to test pipeline locally
    dataset_name='taxi_rides',
)

pipeline = dlt.pipeline(
    pipeline_name="taxi_data",
    destination="bigquery",
    dataset_name="taxi_rides",
    dev_mode=True,
)

info = pipeline.run(ny_taxi)
print(info)