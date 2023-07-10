# Create your views here.
import os

import requests


class CurseForgeAPI:
    MOD_LOADERS = {
        'ANY': 0,
        'FORGE': 1,
        'CAULDRON': 2,
        'LITELOADER': 3,
        'FABRIC': 4,
        'QUILT': 5
    }

    BASE_URL = os.getenv('BASE_URL')

    def __init__(self):
        self.BASE_URL = CurseForgeAPI.BASE_URL
        self.HEADERS = {
            'Accept': 'application/json',
            'x-api-key': f"{os.getenv('API_KEY')}"
        }
        self.PARAMS = {
            'gameId': 432,
        }
        self.GAME_VERSION = None
        self.MOD_LOADER = None

    def switch_game_version(self, game_version):
        self.GAME_VERSION = game_version

    def switch_mod_loader(self, mod_loader):
        self.MOD_LOADER = self.MOD_LOADERS[mod_loader]

    def get_mod_files(self, mod_id):
        params = {
            "modId": mod_id,
            "gameVersion": self.GAME_VERSION,
            "modLoaderType": self.MOD_LOADER,
            "pageSize": 1
        }
        return self.request(url=f"/mods/{mod_id}/files", params=params).json()

    def search_mod_by_name_params(self, mod_name="", pagination=1):
        params = {
            'gameVersion': self.GAME_VERSION,
            'searchFilter': mod_name,
            'modLoaderType': 1,
            'classId': 6,
            'sortField': 1,
            'pageSize': 5,
            'sortOrder': 'desc',
            'index': (pagination - 1) * 5
        }

        return params

    def request(self, url="/", params=None, pagination=0):

        if params is not None:
            params.update(self.PARAMS)
        else:
            params = self.PARAMS

        return requests.get(f"{self.BASE_URL}{url}", params=params, headers=self.HEADERS)

    def search_mods_by_name(self, mod, pagination=1):
        param = self.search_mod_by_name_params(mod_name=mod, pagination=pagination)
        return self.request(url='/mods/search', params=param)

    @staticmethod
    def return_mod_loaders():
        return {
            "Any": 0,
            "Forge": 1,
            "Cauldron": 2,
            "LiteLoader": 3,
            "Fabric": 4,
            "Quilt": 5
        }

    @staticmethod
    def return_game_versions():
        data = requests.get(f"{CurseForgeAPI.BASE_URL}/minecraft/version").json()['data']
        versions = [x['versionString'] for x in data]
        return versions
