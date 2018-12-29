from urllib.parse import urlparse, urljoin
from flask import request
from pathlib import Path
from ruamel.yaml import YAML


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def parse_pricing():
    yaml = YAML(typ='safe')
    file = Path('pricing.yaml')
    if file.is_file():
        pricing = file
    else:
        pricing = Path('pricing.yaml.sample')
    with open(pricing) as f:
        levels = yaml.load(f)
    return levels


def levels_to_plans(price_levels):
    price_plans = {}
    for value in price_levels.values():
        price_plans[value['name']] = value['price']
