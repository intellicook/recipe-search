import os
import sys

from tests.mocks import domain_controllers

os.environ["_TESTING"] = "True"

# Mock imports
sys.modules["domain.controllers"] = domain_controllers
