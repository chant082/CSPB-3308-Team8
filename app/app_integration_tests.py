###############################################################################
## This Python script performs integration tests for the Flask application
## This uses Python's unittest framework and Flask's test client
## CSPB 3308 Summer 2026
## Author: Team Infinity(Team 8) - Craig
##
###############################################################################

import os
import unittest

import app as app_module
import create_db


TEST_DB_NAME = "integration_test.db"

# Create a fresh integration_test.db 

class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

        create_db.create_table(TEST_DB_NAME)

        app_module.DATABASE_NAME = TEST_DB_NAME

        self.client = app_module.app.test_client()

    def tearDown(self):
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)

    def test_profile_redirects_to_login_when_logged_out(self):
        response = self.client.get("/profile")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
