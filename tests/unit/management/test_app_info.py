import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

from flask_management_blueprint.management import AppInfo
from flask_management_blueprint.management.health_status import OK, PARTIALLY_OK, CRITICAL


def healthy():
    return True


def unhealthy():
    return False


def very_unhealthy():
    raise Exception("Service Unavailable")


class TestAppInfo(TestCase):

    def setUp(self):
        AppInfo.RESOURCES = []
        AppInfo.CONFIG = {}

    def test_register_resource(self):
        self.assertEqual(AppInfo.RESOURCES, [])

        AppInfo.register_resource(healthy)

        self.assertEqual(AppInfo.RESOURCES, [healthy])

    def test_app_status_ok(self):
        AppInfo.register_resource(healthy)
        AppInfo.register_resource(healthy)

        self.assertEqual(AppInfo.app_status(), OK)

    def test_app_status_ok_without_resources(self):
        self.assertEqual(AppInfo.app_status(), OK)

    def test_app_status_partially_ok(self):
        AppInfo.register_resource(healthy)
        AppInfo.register_resource(unhealthy)

        self.assertEqual(AppInfo.app_status(), PARTIALLY_OK)

    def test_app_status_critical(self):
        AppInfo.register_resource(unhealthy)
        AppInfo.register_resource(unhealthy)

        self.assertEqual(AppInfo.app_status(), CRITICAL)

    def test_app_status_very_sick(self):
        AppInfo.register_resource(very_unhealthy)
        AppInfo.register_resource(very_unhealthy)

        self.assertEqual(AppInfo.app_status(), CRITICAL)

    @patch("builtins.open")
    def test_read_config_ok(self, mock_open):
        os.environ["CONFIG_FILE_PATH"] = ""

        m = MagicMock()
        e = MagicMock()
        e.read.return_value = "{\"a\": 1}"
        m.__enter__.return_value = e

        mock_open.return_value = m

        AppInfo.read_config()
        self.assertEqual(AppInfo.CONFIG, {"a": 1})

    @patch("builtins.open")
    def test_read_config_not_ok(self, mock_open):
        os.environ["CONFIG_FILE_PATH"] = ""

        m = MagicMock()
        e = MagicMock()
        e.read.return_value = "{\"a:\" 1}"
        m.__enter__.return_value = e

        mock_open.return_value = m

        AppInfo.read_config()
        self.assertEqual(AppInfo.CONFIG, {})

    @patch("flask_management_blueprint.management.AppInfo.app_status")
    @patch("flask_management_blueprint.management.AppInfo.read_config")
    def test_app_info_no_config(self, mock_read, mock_status):
        mock_status.return_value = OK
        actual = AppInfo.app_info()

        self.assertEqual(actual["ApplicationName"], "Unknown")
        self.assertEqual(actual["ApplicationType"], "Unknown")
        self.assertEqual(actual["BuildDate"], "Unknown")
        self.assertEqual(actual["Version"], "Unknown")
        self.assertEqual(actual["Status"], OK[0])
        self.assertEqual(actual["StatusName"], OK[1])

    @patch("flask_management_blueprint.management.AppInfo.app_status")
    @patch("flask_management_blueprint.management.AppInfo.read_config")
    def test_app_info_with_config(self, mock_read, mock_status):
        AppInfo.CONFIG = {
            "ApplicationName": "mock1",
            "ApplicationType": "mock2",
            "BuildDate": "mock3",
            "Version": "mock4"
        }

        mock_status.return_value = PARTIALLY_OK
        actual = AppInfo.app_info()

        self.assertEqual(actual["ApplicationName"], "mock1")
        self.assertEqual(actual["ApplicationType"], "mock2")
        self.assertEqual(actual["BuildDate"], "mock3")
        self.assertEqual(actual["Version"], "mock4")
        self.assertEqual(actual["Status"], PARTIALLY_OK[0])
        self.assertEqual(actual["StatusName"], PARTIALLY_OK[1])
