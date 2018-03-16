from unittest import TestCase

from aioresponses import aioresponses
import asyncio

from flask_management_blueprint.management import HealthCheck


class TestHealthCheck(TestCase):

    def setUp(self):
        HealthCheck.RESOURCES = []

    @aioresponses()
    def test_check_resources_health(self, mock):
        HealthCheck.register_resource(
            "resource1", "http://mock.com/health-check")

        mock.get("http://mock.com/health-check", status=200,
                 payload={"success": False})

        actual = HealthCheck.check_resources_health()

        expected = [{"success": False}]

        self.assertEqual(actual, expected)

    @aioresponses()
    def test_check_multiple_resources_health(self, mock):
        HealthCheck.register_resource(
            "resource1", "http://mock.com/health-check")
        mock.get("http://mock.com/health-check", status=200,
                 payload={"success": True})

        HealthCheck.register_resource(
            "resource2", "http://patch.com/health-check")
        mock.get("http://patch.com/health-check", status=200,
                 payload={"success": False, "dependencies": False})

        HealthCheck.register_resource(
            "resource3", "http://dunno.com/health-check")
        mock.get("http://dunno.com/health-check", status=500,
                 payload={"message": "Internal Error"})

        actual = HealthCheck.check_resources_health()

        expected = [
            {"success": True},
            {"success": False, "dependencies": False},
            {"message": "Internal Error"}
        ]

        self.assertEqual(actual, expected)
