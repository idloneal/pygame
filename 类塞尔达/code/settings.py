# game setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 64
HITBOX_OFFSET = {
    'player': (0, -30),
    'object': (0, -80),
    'grass': (0, -20),
    'invisible': (-20, 20),

}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#484855'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = '#fe0059'
ENERGY_COLOR = '#609dff'
UI_BORDER_COLOR_ACTIVE = '#fcff20'

# upgrade menu
TEXT_COLOR_SELECTED = '#ffad5d'
BAR_COLOR = '#111111'
BAR_COLOR_SELECTED = '#fcff20'
UPGRADE_BG_COLOR_SELECTED = '#666666'
# weapons
WEAPON_DATA = {
    'sword': {'cooldown': 200, 'damage': 15, 'graphics': '../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 600, 'damage': 50, 'graphics': '../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 1100, 'damage': 140, 'graphics': '../graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 100, 'damage': 8, 'graphics': '../graphics/weapons/rapier/full.png'},
    'trident': {'cooldown': 160, 'damage': 10, 'graphics': '../graphics/weapons/trident/full.png'},
}

# magic
MAGIC_DATA = {
    'flame': {'mana': 5, 'cost': 20, 'graphics': '../graphics/particles/flame/fire.png'},
    'heal': {'mana': 20, 'cost': 10, 'graphics': '../graphics/particles/heal/heal.png'}
}

# enemy
ENEMY_DATA = {
    'squid': {'health': 200, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
              'attack_sound': '../audio/attack/slash.wav', 'speed': 6, 'resistance': 3, 'attack_radius': 80,
              'notice_radius': 360},
    'raccoon': {'health': 1000, 'exp': 400, 'damage': 50, 'attack_type': 'claw',
                'attack_sound': '../audio/attack/claw.wav', 'speed': 5, 'resistance': 1, 'attack_radius': 120,
                'notice_radius': 400},
    'spirit': {'health': 200, 'exp': 110, 'damage': 8, 'attack_type': 'thunder',
               'attack_sound': '../audio/attack/fireball.wav', 'speed': 5, 'resistance': 2, 'attack_radius': 60,
               'notice_radius': 350},
    'bamboo': {'health': 140, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack',
               'attack_sound': '../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50,
               'notice_radius': 300},
}
