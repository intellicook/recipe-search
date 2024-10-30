import os
import sys

os.environ["_TESTING"] = "True"

from tests.mocks import domain_controllers  # noqa: E402

# Mock imports
sys.modules["domain.controllers"] = domain_controllers
