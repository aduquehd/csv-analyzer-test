from config import celery_app

from csv_analyzer.apps.dataset.models import DataSetFiles
from csv_analyzer.apps.mongodb.utils import MongoDBConnection

from csv_analyzer.apps.dataset.utils.analyze_file import analyze_file


@celery_app.task()
def populate_dataset_file(dataset_file_id):
    """
    Populate dataset file data into MongoDB database.
    :param dataset_file_id: String, dataset file ID.
    :return: Count of documents saved.
    """
    dataset_file = DataSetFiles.objects.get(id=dataset_file_id)

    documents = analyze_file(dataset_file)

    mongo_client = MongoDBConnection()
    delete_query = {"data_set_file_id": dataset_file_id}

    mongo_client.delete_bulk(query=delete_query)
    mongo_client.delete_bulk(query={})
    mongo_client.insert_record_bulk(documents=documents)

    dataset_file.is_analyzed = True
    dataset_file.save()

    return len(documents)
