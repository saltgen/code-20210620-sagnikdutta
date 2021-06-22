
from pymongo import MongoClient
from bson.objectid import ObjectId

from .constants import logger


class DBHandler:

	def __init__(self):
		self.db_connection = MongoClient(
			host='db_host',
			port=27017,
			username='root',
			password='pass',
			authSource='admin'
		)
		self.db_client = self.db_connection.health_reports
		
	def __del__(self):
		self.db_connection.close()  # In order to close db connections before exiting
		logger.info("Successfully disconnected from database")
		
	def get_data_in_collection(self, collection_name):
		return self.db_client[collection_name].find()
	
	def update_patient_record(self, collection_name, document_id, json_data):

		collection = self.db_client[collection_name]
		try:
			collection.update_one(
				{"_id": ObjectId(document_id)},
				{"$set": json_data}
			)
		except Exception as e:
			logger.error(f"Failed to update document in {collection_name}, error: {e}")
			return False
		return True

	def add_patient_record(self, collection_name, patient_data):
		collection = self.db_client[collection_name]
		try:
			collection.insert_one(patient_data)
		except Exception as e:
			logger.error(f"Failed to add document in {collection_name}, error: {e}")
			return False
		return True
	
	def delete_patient_record(self, collection_name, document_id):
		collection = self.db_client[collection_name]
		try:
			collection.delete_one({"_id": ObjectId(document_id)})
		except Exception as e:
			logger.error(f"Failed to delete document in {collection_name}, error: {e}")
			return False
		return True


db_instance = DBHandler()
