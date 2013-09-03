# # Test OpenTripPlanner
import requests
import urllib

from datetime import datetime
from test_base import TestBase


class TestClass(TestBase):

    def __init__(self, *args, **kwargs):
        super(TestClass, self).__init__(*args, **kwargs)

    def preprocess_test(self, test):
        return test

    def plan_trip(self, test):
        return None
