import pytest
import pytest_flask
from hawkeye import app
from flask import url_for

class TestApp:

	# Canteen View Start
	def test_index(self, client):
		res = client.get(url_for('home'))
		assert res.status_code == 200
	
	def test_elements(self, client):
		res = client.get(url_for('patient'))
		assert res.status_code == 302

	