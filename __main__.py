"""A Python Pulumi program that creates pingdom monitoring resource"""
from pingdom_dynamic_provider import PingDomSchema, PingDomSchemaInputs
from pulumi import Config

config = Config()
region = config.require('region')
endpoints = config.require_object('endpoints')

for endpoint in endpoints:
    PingDomSchema(name=f'pulumi-{region}-{endpoint}',
                  args=PingDomSchemaInputs(
                      endpoint=endpoint,
                      region=region
                  ))

