import binascii
import os
from typing import Optional

from pulumi import Input, Output
from pulumi.dynamic import ResourceProvider, CreateResult, DiffResult, UpdateResult, Resource
from pingdom_ops import get_pingdom_check, get_client
from valult_helper import get_vault_secrets


class PingDomSchemaInputs(object):
    endpoint_id: Input[str]

    def __init__(self, endpoint, region):
        self.endpoint = endpoint
        self.region = region


class PingDomSchemaProvider(ResourceProvider):
    def create(self, args):
        get_client(get_vault_secrets(path='pingdom')['apikey']).create_check(
            get_pingdom_check(endpoint=args['endpoint'], region=args['region']))
        return CreateResult("schema-" + binascii.b2a_hex(os.urandom(16)).decode("utf-8"), outs=args)

    def diff(self, id, oldInputs, newInputs):
        replaces = []
        if (oldInputs["endpoint"] != newInputs["endpoint"]): replaces.append("endpoint")
        if (oldInputs["region"] != newInputs["region"]): replaces.append("region")
        return DiffResult(
            changes=oldInputs != newInputs,
            replaces=replaces,
            stables=None,
            delete_before_replace=True)

    def update(self, id, oldInputs, newInputs):
        return UpdateResult(outs={**newInputs})

    def delete(self, id, args):
        client = get_client(get_vault_secrets(path='pingdom')['apikey'])
        check = [check for check in client.get_checks() if check['hostname'] == args['endpoint']]
        if check:
            client.delete_check(check.pop()['id'])


class PingDomSchema(Resource):
    endpoint: Output[str]
    region: Output[str]

    def __init__(self, name: str, args: PingDomSchemaInputs, opts=None):
        super().__init__(PingDomSchemaProvider(), name, vars(args), opts)
