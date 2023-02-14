import os
from pymongo import MongoClient
from dotenv import load_dotenv

from logger import logger, werk_logger

load_dotenv()


class MongoDBHandler(object):

    def __init__(self):
        #client = MongoClient(os.getenv('MONGO_CLIENT'))
        #database = client[os.getenv('DB')]
        client = MongoClient("localhost", 27017, maxPoolSize=50)
        database = client['admin']
        self.collection = database['users']

    def read(self, query_params: dict):

        logger.debug('Reading data from the DB...')

        try:
            documents = self.collection.find(query_params)
            output = [{item: data[item] for item in data if item != '_id'} for data in documents]

            if len(output) == 1:
                output = output[0]

            logger.debug('read - Success')

        except Exception as err:
            output = {'status': 'Fail',
                    'error': err}
            logger.error(f'insert - {err}')

        return output

    def insert(self, data: dict):

        logger.debug('Inserting data to the DB...')

        try:
            response = self.collection.insert_one(data)
            output = {'status': 'Success',
                    'Document_ID': str(response.inserted_id)}
            logger.debug('insert - Success')

        except Exception as err:
            output = {'status': 'Fail',
                    'error': err}
            logger.error(f'insert - {err}')

        return output

    def update(self, query_params: dict, updated_data: dict):
        logger.debug('Updating data on the DB...')
        response = self.collection.update_one(query_params, {"$set": updated_data})
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, query_params: dict):
        logger.debug('Deleting data from the DB...')
        response = self.collection.delete_one(query_params)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
