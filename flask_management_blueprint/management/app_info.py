"""Module to define classes to retrieve app info"""
import datetime
import json
import os
import platform
import socket

from .health_status import OK, PARTIALLY_OK, CRITICAL

class AppInfo(object):
    """Class to define methods to manage app-info"""

    RESOURCES = []
    CONFIG = {}

    @classmethod
    def app_status(cls):
        """Method to check app_status accordingly to resources' health
        """

        healthy = 0
        for resource in cls.RESOURCES:
            try:
                if resource() is True:
                    healthy += 1
            except Exception as exc:
                # TODO logar exception
                print(exc)
        if len(cls.RESOURCES) == healthy:
            return OK
        if healthy == 0:
            return CRITICAL
        else:
            return PARTIALLY_OK
            
    @classmethod
    def register_resource(cls, resource):
        """Method to register a resource necessary to the app

        Args:
            resource (func): A function to check the resource health
                             that returns True/False
        """

        cls.RESOURCES.append(resource)

    @classmethod
    def read_config(cls):
        """Method to read the app-config
        """

        file_path = os.environ.get("CONFIG_FILE_PATH", "./config.json")
        try:
            with open(file_path, 'r') as config_file:
                cls.CONFIG = json.load(config_file)
        except (IOError, ValueError) as exc:
            # TODO logar exception
            print(exc)

    @classmethod
    def app_info(cls):
        """Method that returns app general info
        """
        if cls.CONFIG == {}:
            cls.read_config()

        status = cls.app_status()
        return {
            "ApplicationName": cls.CONFIG.get("ApplicationName", "Unknown"),
            "ApplicationType": cls.CONFIG.get("ApplicationType", "Unknown"),
            "BuildDate": cls.CONFIG.get("BuildDate", "Unknown"),
            "MachineName": socket.gethostname(),
            "OS": {
                "Name": os.name,
                "Version": '{} {}'.format(platform.system(),
                                          platform.release())
            },
            "Status": status[0],
            "StatusName" : status[1],
            "Timestamp": datetime.datetime.now().isoformat(),
            "Version": cls.CONFIG.get("Version", "Unknown"),
        }
