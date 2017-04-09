import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')


def aws_access_key_id():
    return parser['credentials']['aws_access_key_id']


def aws_secret_access_key():
    return parser['credentials']['aws_secret_access_key']


def endpoint():
    return parser['nectar']['endpoint']


def endpoint_path():
    return parser['nectar']['endpoint_path']


def region():
    return parser['nectar']['region']


def port():
    return parser['nectar']['port']


def default_instance_name():
    return parser['default']['instance_name']


def default_image_id():
    return parser['default']['image_id']


def default_key_name():
    return parser['default']['key_name']


def default_instance_type():
    return parser['default']['instance_type']


def default_security_groups():
    return json.loads(parser['default']['security_groups'])
