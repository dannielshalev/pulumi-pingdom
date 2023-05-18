import os
import hvac


def get_vault_secrets(path):
    client = hvac.Client(token=os.environ['VAULT_TOKEN'])
    return client.secrets._kv.v2.read_secret_version(path=path, mount_point='testkeys')['data']['data']
