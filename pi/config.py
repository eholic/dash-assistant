import os
import uuid
import yaml

class Config:
    DEVICE_ID = os.getenv('DEVICE_ID', str(uuid.uuid1()))
    DEVICE_MODEL_ID = os.getenv('DEVICE_MODEL_ID')
    if DEVICE_MODEL_ID is None:
        raise Exception('DEVICE_MODEL_ID is missing.')
    CREDENTIALS = os.getenv('CREDENTIALS',
                            os.path.join(os.getenv('HOME', ''), '.config/google-oauthlib-tool/credentials.json'))

    if os.path.exists('dashes.local.yml'):
        dash_yml = 'dashes.local.yml'
    elif os.path.exists('dashes.yml'):
        dash_yml = 'dashes.yml'
    else:
        raise Exception('dashes.yml is missing')
    with open(dash_yml, 'r') as f:
        actions = yaml.safe_load(f)['actions']

