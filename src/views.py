import json
from flask import Response
from flask_restful import Resource, reqparse

from .utils import compute_bmi_data
from .db_handler import db_instance


class bmiResultsAPI(Resource):
	
	def get(self):
		"""
		Get patient records with bmi data
		:return: json
		"""
		response_data = []
		collection_cursor = db_instance.get_data_in_collection('bmi_records')
		
		for record in collection_cursor:
			
			if 'BMIKg/m2' not in record:
				bmi_data = compute_bmi_data(record, update_document=True)
				record.update(bmi_data)
				
			record["_id"] = str(record["_id"])
			response_data.append(record)
		
		response_data.append({"meta": {"count": len(response_data)}})
		
		try:
			resp = Response(json.dumps(response_data), status=200, mimetype='application/json')
		except Exception as e:
			error_msg = json.dumps({'error_msg': f"Failed to fetch bmi data, error: {e}"})
			resp = Response(error_msg, status=400, mimetype='application/json')
			
		return resp
	

class obesityDataAPI(bmiResultsAPI, Resource):
	
	def get(self):
		"""
		Get patient records with obesity
		:return: json
		"""
		bmi_records_response = super().get().json
		bmi_records_response.pop(-1)  # Removing 'meta' dict from json response
		
		response_data = [
			_record
			for _record in bmi_records_response
			if _record['BMICategory'] not in ['Underweight', 'Normal weight']
		]
		response_data.append({"meta": {"count": len(response_data)}})
		
		try:
			resp = Response(json.dumps(response_data), status=200, mimetype='application/json')
		except Exception as e:
			error_msg = json.dumps({'error_msg': f"Failed to fetch obesity data, error: {e}"})
			resp = Response(error_msg, status=400, mimetype='application/json')

		return resp
	
	
class addPatientDataAPI(Resource):
	
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'Gender',
			type=str,
			required=True,
			location='json'
		)
		self.reqparse.add_argument(
			'HeightCm',
			type=float,
			required=True,
			location='json'
		)
		self.reqparse.add_argument(
			'WeightKg',
			type=float,
			required=True,
			location='json'
		)
		self.args = self.reqparse.parse_args()
	
	def post(self):
		"""
		Add a patient record to db
		:return: None
		"""
		
		bmi_data = compute_bmi_data(self.args)
		self.args.update(bmi_data)
		
		if db_instance.add_patient_record('bmi_records', self.args):
			msg = json.dumps({"msg": "Added patient data successfully!"})
			resp = Response(msg, status=204, mimetype='application/json')
		else:
			error_msg = json.dumps({'error_msg': "Failed to add patient data"})
			resp = Response(error_msg, status=400, mimetype='application/json')

		return resp
