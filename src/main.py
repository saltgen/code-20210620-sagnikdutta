
from flask import Flask, redirect
from flask_restful import Api

from .views import bmiResultsAPI, obesityDataAPI, addPatientDataAPI


def create_app():
	app = Flask(__name__)
	api = Api(app)
	
	@app.route('/')
	def redirect_to_bmi_endpoint():
		return redirect('/bmi-records', code=302)
	
	api.add_resource(bmiResultsAPI, '/bmi-records', endpoint='bmiResults')
	api.add_resource(obesityDataAPI, '/obesity-data', endpoint='obesityData')
	api.add_resource(addPatientDataAPI, '/add-patient-data', endpoint='addPatientData')

	return app


if __name__ == '__main__':
	flask_app = create_app()
	flask_app.run(host="127.0.0.1", port=5000, debug=True)
