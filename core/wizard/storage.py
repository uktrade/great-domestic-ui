import copy
from django.core.cache import cache
from formtools.wizard.storage import BaseStorage

WIZARD_CACHE_TIMEOUT = 2592000  # 30 days


class CacheStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.load_data()
        if self.data is None:
            self.init_data()

        self.initial_data = copy.deepcopy(self.data)

    def load_data(self):
        return cache.get(self.prefix)

    def update_response(self, response):
        super().update_response(response)
        if self.data != self.initial_data:
            cache.set(self.prefix, self.data, WIZARD_CACHE_TIMEOUT)
