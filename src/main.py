import os
import sys
import json

import system

_Debug = True


ROOT_PATH = ''

if system.is_android():
    ROOT_PATH = os.path.abspath(os.environ['ANDROID_ARGUMENT'])
elif system.is_osx():
    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
elif system.is_ios():
    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
else:
    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


from kivy.config import Config
Config.set('graphics', 'top', '100')
Config.set('graphics', 'left', '100')
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '700')


from kivy.core.window import Window
from kivy.app import App

import res
import rend
import dat
import scen


class WorldsApp(App):

    known_templates = {}
    known_figures_parts = {}

    def __init__(self, **kwargs):
        self.root_path = ROOT_PATH
        self.data_path = system.get_app_data_path()
        res.DATA_PATH = self.data_path
        if _Debug:
            print('WorldsApp.__init__ root_path=%r data_path=%r' % (self.root_path, self.data_path))
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        super().__init__(**kwargs)

    def build(self):
        catalog = dat.CatalogData()
        catalog.load_figures(figures_file_name=res.data_path('catalog/figures.json'))
        catalog.load_animations(animations_file_name=res.data_path('catalog/animations.json'))
        catalog.load_armors(armors_file_name=res.data_path('catalog/armors.json'))
        catalog.load_weapons(weapons_file_name=res.data_path('catalog/weapons.json'))
        catalog.load_materials(materials_file_name=res.data_path('catalog/materials.json'))
        land = dat.LandData()
        land.load_heightmap_file(heightmap_file_name=res.data_path('assets/heightmap.png'))
        land.load_tilemap_file(tilemap_file_name=res.data_path('assets/encoded.png'))
        land.load_cache_tiles_textures(textures_dir_path=res.data_path('assets/land'))
        land.load_plants_data(plants_data_file_name=res.data_path('assets/plants.json'))
        land.load_buildings_data(buildings_data_file_name=res.data_path('assets/buildings.json'))
        scene = scen.Scene(land=land, catalog=catalog)
        scene.calculate_land_vertices()
        scene.calculate_scaled_elevation_map()
        renderer = rend.Renderer(app_root=self, scene=scene)
        self.known_templates = json.loads(open(res.data_path('catalog/figures_samples.json'), 'rt').read())
        scene.renderer = renderer
        scene.init_scene(257, 340)
        # scene.init_scene()
        # self.create_human_hero(scene)
        scene.create_hero(
            # model_name='unorma', weapon='stone battle axe.granite',
            # model_name='unmogo', texture='goblin00',
            # model_name='unmori', texture='rick',
            # model_name='unmosu', texture='succubus02',
            # model_name='unmotr', texture='troll02',
            model_name='unhuma',
            skin=41,
            hair=0,
            wears=[
              "hadagan brigand pants.thin",
              "hadagan brigand boots.thin",
              "hadagan brigand gloves.thin",
              "hadagan brigand leggins.thick",
              "hadagan brigand helm.thick",
              "hadagan brigand plate.thick"
            ],
            weapon='cheat dagger.bronze',
            # elevation_correction=0.5,
        )
        return renderer


def main():
    # url_prefix = 'https://raw.githubusercontent.com/eigamer/ei/refs/heads/main/eng2001/res/'
    # url_prefix = 'https://raw.githubusercontent.com/eigamer/ei/refs/heads/main/astral2006/res/'
    res.download_file('data', 'figures.res', ['figures_res_0', 'figures_res_1', ], 'https://raw.githubusercontent.com/eigamer/ei/refs/heads/main/astral2006/res/')
    res.download_file('data', 'textures.res', ['textures_res_0', 'textures_res_1', 'textures_res_2', ], 'https://raw.githubusercontent.com/eigamer/ei/refs/heads/main/astral2006/res/')
    res.download_file('data', 'redress.res', ['redress_res_0', 'redress_res_1', ], 'https://raw.githubusercontent.com/eigamer/ei/refs/heads/main/astral2006/res/')
    res.download_file('catalog', 'animations.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'armors.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'buildings.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'figures.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'figures_names.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'figures_parts.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'figures_samples.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'materials.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'plants.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'textures.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    res.download_file('catalog', 'weapons.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/catalog/')
    for i in range(0, 28):
        res.download_file('assets/land', f'{i}.png', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/land/')
    res.download_file('assets', 'water8a.png', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    # TODO: the following needs to move from "assets" to "map" sub dir
    res.download_file('assets', 'tiles.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'catalog.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'map.png', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'heightmap.png', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'encoded.png', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'plants.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    res.download_file('assets', 'buildings.json', [], 'https://raw.githubusercontent.com/bitdust-io/worlds/refs/heads/main/assets/')
    WorldsApp().run()


if __name__ == '__main__':
    main()
