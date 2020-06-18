from http import HTTPStatus
from unittest.mock import patch

from flask_management_blueprint.management import health_status
from flask_management_blueprint.management import management_resource


@patch('flask_management_blueprint.management.management_resource.HealthCheck.check_resources_health')
@patch('flask_management_blueprint.management.management_resource.AppInfo.app_info')
def test_health_check_is_ok(mock_app_info, mock_health_check, test_app):
    with test_app.test_request_context():
        mock_health_check.return_value = []
        mock_app_info.return_value = {
            "ApplicationName": "mock1",
            "ApplicationType": "mock2",
            "BuildDate": "mock3",
            "Version": "mock4",
            "Status": health_status.OK[0]
        }

        response = management_resource.health_check()

        assert response[1] is HTTPStatus.OK


@patch('flask_management_blueprint.management.management_resource.HealthCheck.check_resources_health')
@patch('flask_management_blueprint.management.management_resource.AppInfo.app_info')
def test_health_check_is_not_ok(mock_app_info, mock_health_check, test_app):
    with test_app.test_request_context():
        mock_health_check.return_value = []
        mock_app_info.return_value = {
            "ApplicationName": "mock1",
            "ApplicationType": "mock2",
            "BuildDate": "mock3",
            "Version": "mock4",
            "Status": health_status.CRITICAL[0]
        }

        response = management_resource.health_check()

        assert response[1] is HTTPStatus.INTERNAL_SERVER_ERROR
