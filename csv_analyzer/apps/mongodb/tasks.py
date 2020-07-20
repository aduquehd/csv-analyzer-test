from config import celery_app


@celery_app.task()
def analyze_dataset_file():
    """A pointless Celery task to demonstrate usage."""

    return None
