
from .db_handler import db_instance


def get_bmi_category(bmi_value):
	
	bmi_category, health_risk = None, None
	if bmi_value <= 18.4:
		bmi_category, health_risk = 'Underweight', 'Malnutrition risk'
	elif 18.5 <= bmi_value <= 24.9:
		bmi_category, health_risk = 'Normal weight', 'Low risk'
	elif 25 <= bmi_value <= 29.9:
		bmi_category, health_risk = 'Overweight', 'Enhanced risk'
	elif 30 <= bmi_value <= 34.9:
		bmi_category, health_risk = 'Moderately obese', 'Medium risk'
	elif 35 <= bmi_value <= 39.9:
		bmi_category, health_risk = 'Severely obese', 'High risk'
	elif bmi_value >= 40:
		bmi_category, health_risk = 'Very severely obese', 'Very high risk'
	
	return bmi_category, health_risk
		

def compute_bmi_data(patient_data, update_document=False):
	"""
	Helps with calculating bmi and adding respective
	columns, optionally can update db record
	:param patient_data: dict
	:param update_document: bool
	:return: dict
	"""
	
	bmi_value = round(patient_data['WeightKg'] / (patient_data['HeightCm']/100), 2)
	bmi_category_results = get_bmi_category(bmi_value)
	bmi_category = bmi_category_results[0]
	health_risk = bmi_category_results[1]
	bmi_columns = {
		"BMIKg/m2": bmi_value,
		"BMICategory": bmi_category,
		"HealthRisk": health_risk
	}
	
	if update_document is True:
		_id = str(patient_data.get("_id", ''))
		db_instance.update_patient_record('bmi_records', _id, bmi_columns)
		
	return bmi_columns
