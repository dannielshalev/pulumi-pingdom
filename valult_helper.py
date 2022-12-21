import hvac
import os


def get_vault_secrets(path):
    client = hvac.Client(url='http://automotive-vault:8200/', token=os.environ['VAULT_TOKEN'])
    return client.secrets._kv.v2.read_secret_version(path=path, mount_point='infraKeys')['data']['data']
