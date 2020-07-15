from config import celery_app


@celery_app.task()
def analyze_dataset_file():
    """A pointless Celery task to demonstrate usage."""
    from csv_analyzer.apps.dataset.models import DataSetFiles, DataSet, DataSetWearerData, Blog

    import uuid

    for i in range(0, 10):
        Blog.objects.using('mongodb').create(
            name="Andres",
            tagline="Software engineer"
        )
        # DataSetWearerData.objects.using('mongodb').create(
        #     air_pressure_9am=38465925,
        #     air_temp_9am=3345725,
        #     avg_wind_direction_9am=4256325,
        #     avg_wind_speed_9am=3256795,
        #     max_wind_direction_9am=3947625,
        #     max_wind_speed_9am=324845,
        #     rain_accumulation_9am=37525,
        #     rain_duration_9am=334625,
        #     relative_humidity_9am=323625,
        #     relative_humidity_3pm=32355,
        # )

    return None
