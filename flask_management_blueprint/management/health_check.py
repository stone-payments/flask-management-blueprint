"""Module to define classes to retrieve app health"""
import asyncio
import async_timeout
import aiohttp


async def fetch(session, url):
    """Method to fetch data from a url asynchronously
    """
    async with async_timeout.timeout(30):
        async with session.get(url) as response:
            return await response.json()


async def execute_request(url):
    """Method to execute a http request asynchronously
    """
    async with aiohttp.ClientSession() as session:
        json = await fetch(session, url)
        return json


class HealthCheck(object):
    """Class to define methods to manage app health"""

    RESOURCES = []

    @classmethod
    def register_resource(cls, name, url):
        """Method to register a resource necessary to the app

        Args:
            name (string): Name of system to check health
            url (string): Url of system to check health
        """

        cls.RESOURCES.append({name: url})

    @classmethod
    def check_resources_health(cls):
        """Method to check the health of all the registered resources
        """

        url_list = [list(rec.values())[0]
                    for rec in cls.RESOURCES]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        resp = loop.run_until_complete(asyncio.gather(
            *[execute_request(url) for url in url_list]
        ))

        return resp
