# from pypingdom import Client
from pingdomv3 import Client


def get_client(secret):
    return Client(token=secret)


def get_pingdom_check(endpoint, region):
    return dict(name=endpoint, type="http", host=endpoint, resolution=1, port=443, encryption=True,
                ssl_down_days_before="21", probe_filters=[f"region:{region}"])
