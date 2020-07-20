from pymongo import MongoClient
import environ

env = environ.Env()


class MongoDBConnection:
    def __init__(self):
        self.client = MongoClient(
            host=env('MONGODB_HOST'),
            username=env('MONGODB_USER'),
            port=int(env('MONGODB_PORT')),
            password=env('MONGODB_PASSWORD'),
            authSource=env('MONGODB_DATABASE'),
            authMechanism='SCRAM-SHA-1'
        )
        self.db = self.client['csv_analyzer_data_sets']

    def get_client(self):
        return self.client

    def get_database(self):
        return self.db

    def insert_record(self, document, collection='data_set_weather_data'):
        collection = self.db[collection]
        collection.insert_one(document)
        return collection

    def insert_record_bulk(self, documents, collection='data_set_weather_data'):
        collection = self.db[collection]
        collection.insert_many(documents)
        return collection

    def delete_bulk(self, query, collection='data_set_weather_data'):
        collection = self.db[collection]
        collection.delete_many(query)

    def get_list(self, query, collection='data_set_weather_data'):
        collection = self.db[collection]
        data = collection.find(query)
        return self._convert_mongodb_data_list_to_python(data)

    @staticmethod
    def _convert_mongodb_data_list_to_python(data):
        list_data = []
        for element in data:
            del element['_id']
            list_data.append(element)
        return list_data
