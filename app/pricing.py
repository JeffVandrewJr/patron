from pathlib import Path
from ruamel.yaml import YAML


class Pricing(object):
    def __init__(self):
        self.price_levels = self._get_price_levels()
        self.price_plans = self._levels_to_plans(self.price_levels)

    def _get_price_levels(self):
        yaml = YAML(typ='safe')
        file = Path('/var/pricing/pricing.yaml')
        if file.is_file():
            pricing = file
        else:
            pricing = Path('pricing.yaml.sample')
        with open(pricing) as f:
            levels = yaml.load(f)
        return levels

    def _levels_to_plans(self, price_levels):
        price_plans = {}
        for value in price_levels.values():
            price_plans[value['name']] = value['price']
        return price_plans
