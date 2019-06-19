from django.test import TestCase
from fraudDetector.models import *
from fraudDetector.fraudDetector import *

# Create your tests here.

class FraudDetectorTests(TestCase):
    def test_trial(self):
        