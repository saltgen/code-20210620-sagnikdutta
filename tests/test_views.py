
import json
import pytest
from flask import url_for

from src.main import create_app
from src.db_handler import db_instance


@pytest.fixture(scope="session")
def app():
	app = create_app()
	return app


def test_get_bmi_results(client):
	"""
	Verifies the data from bmi-records/ endpoint
	:param client: fixture
	:return: None
	"""
	response = client.get(url_for('bmiResults'))
	response_json = response.json
	response_json.pop(-1)  # Removing meta dict
	assert response.status_code == 200
	for item in response_json:
		assert 'BMIKg/m2' in item
		assert 'BMICategory' in item
		assert 'HealthRisk' in item
		

def test_validate_obesity_data(client):
	"""
	Verifies the data from obesity-data endpoint
	against all data in db.
	For proper testing, add a patient record with sample data below
	POST /add-patient-data
	data = {
		"Gender": "Male",
		"HeightCm": 175,
		"WeightKg": 40
	}
	:param client: fixture
	:return: None
	"""
	filtered_data_from_db = [
		record
		for record in list(db_instance.get_data_in_collection('bmi_records'))
		if record['BMICategory'] not in ['Underweight', 'Normal weight']
	]
	response = client.get(url_for('obesityData'))
	response_json = response.json
	response_json.pop(-1)  # Removing meta dict
	assert len(filtered_data_from_db) == len(response_json)
	
	
def test_add_patient_data_positive(client):
	"""
	Happy path test for patient data
	:param client: fixture
	:return: None
	"""
	mimetype = 'application/json'
	headers = {
		'Content-Type': mimetype,
		'Accept': mimetype
	}
	data = {
		"Gender": "Male",
		"HeightCm": 175,
		"WeightKg": 40
	}
	response = client.post(url_for('addPatientData'), data=json.dumps(data), headers=headers)
	assert response.status_code == 204
	# teardown process
	response = client.get(url_for('bmiResults'))
	response_json = response.json
	response_json.pop(-1)  # Removing meta dict
	test_document_id = str(response_json[-1]["_id"])
	db_instance.delete_patient_record('bmi_records', test_document_id)
	
	
def test_add_patient_data_missing_attribute(client):
	"""
	Sad path test for patient data
	when attribute is missing
	:param client: fixture
	:return: None
	"""
	mimetype = 'application/json'
	headers = {
		'Content-Type': mimetype,
		'Accept': mimetype
	}
	data = {
		"Gender": "Male",
		"HeightCm": 175,  # Incorrect value type
	}
	response = client.post(url_for('addPatientData'), data=json.dumps(data), headers=headers)
	assert response.status_code == 400
	
	
def test_add_patient_data_incorrect_attribute_type(client):
	"""
	Sad path test for patient data
	when attribute value type is incorrect
	:param client: fixture
	:return: None
	"""
	mimetype = 'application/json'
	headers = {
		'Content-Type': mimetype,
		'Accept': mimetype
	}
	data = {
		"Gender": "Male",
		"HeightCm": "hi",  # Incorrect value type
		"WeightKg": 50
	}
	response = client.post(url_for('addPatientData'), data=json.dumps(data), headers=headers)
	assert response.status_code == 400
