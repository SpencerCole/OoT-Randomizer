import collections
import logging


def set_rules(world):
    global_rules(world)

    #if world.goal == 'dungeons':
        # require all dungeons to beat ganon
        #add_rule(world.get_location('Ganon'), lambda state: state.can_reach('Master Sword Pedestal', 'Location') and state.has('Beat Agahnim 1') and state.has('Beat Agahnim 2'))
    #elif world.goal == 'ganon':
        # require aga2 to beat ganon
        #add_rule(world.get_location('Ganon'), lambda state: state.has('Beat Agahnim 2'))


def set_rule(spot, rule):
    spot.access_rule = rule

def set_always_allow(spot, rule):
    spot.always_allow = rule


def add_rule(spot, rule, combine='and'):
    old_rule = spot.access_rule
    if combine == 'or':
        spot.access_rule = lambda state: rule(state) or old_rule(state)
    else:
        spot.access_rule = lambda state: rule(state) and old_rule(state)


def forbid_item(location, item):
    old_rule = location.item_rule
    location.item_rule = lambda i: i.name != item and old_rule(i)


def item_in_locations(state, item, locations):
    for location in locations:
        if item_name(state, location) == item:
            return True
    return False

def item_name(state, location):
    location = state.world.get_location(location)
    if location.item is None:
        return None
    return location.item.name


def global_rules(world):
    # ganon can only carry triforce
    world.get_location('Ganon').item_rule = lambda item: item.name == 'Triforce'

    # these are default save&quit points and always accessible
    world.get_region('Links House').can_reach = lambda state: True

    # overworld requirements
    set_rule(world.get_entrance('Deku Tree'), lambda state: state.has('Kokiri Sword') or world.open_forest)
    set_rule(world.get_entrance('Lost Woods Bridge'), lambda state: state.has('Kokiri Emerald') or world.open_forest)
    set_rule(world.get_entrance('Deku Tree Basement Path'), lambda state: state.has('Slingshot'))
    set_rule(world.get_location('Heart Piece Grave Chest'), lambda state: state.has('Suns Song'))
    set_rule(world.get_entrance('Composer Grave'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Composer Grave Chest'), lambda state: state.has_fire_source())
    set_rule(world.get_entrance('Bottom of the Well'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_location('Bottom of the Well Front Left Hidden Wall'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Front Center Bombable'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Right Bottom Hidden Wall'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Center Large Chest'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Center Small Chest'), lambda state: state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Back Left Bombable'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Defeat Boss'), lambda state: state.has('Zeldas Lullaby') and state.has('Kokiri Sword')) #Sword not strictly necessary but frankly being forced to do this with sticks isn't fair
    set_rule(world.get_location('Bottom of the Well Invisible Chest'), lambda state: state.has('Zeldas Lullaby') and state.has('Lens of Truth') and state.has('Magic Meter'))
    set_rule(world.get_location('Bottom of the Well Underwater Front Chest'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Bottom of the Well Underwater Left Chest'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Bottom of the Well Basement Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Bottom of the Well Locked Pits'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag') or (state.has('Lens of Truth') and state.has('Magic Meter')))) #It's not fair to have to navigate invisible pits AND forced s&q if you fall.
    set_rule(world.get_location('Bottom of the Well Behind Right Grate'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag') or (state.has('Lens of Truth') and state.has('Magic Meter'))))
    set_rule(world.get_entrance('Death Mountain Entrance'), lambda state: state.has('Zeldas Letter') or state.is_adult())
    set_rule(world.get_location('Death Mountain Bombable Chest'), lambda state: state.can_blast())
    set_rule(world.get_location('Goron City Leftmost Maze Chest'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade', 2) or state.has('Hammer')))
    set_rule(world.get_location('Goron City Left Maze Chest'), lambda state: state.can_blast() or (state.has('Progressive Strength Upgrade', 2) and state.is_adult()))
    set_rule(world.get_location('Goron City Right Maze Chest'), lambda state: state.can_blast() or (state.has('Progressive Strength Upgrade', 2) and state.is_adult()))
    set_rule(world.get_entrance('Darunias Chamber'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_location('Darunias Joy'), lambda state: state.has('Sarias Song'))
    set_rule(world.get_entrance('Goron City from Woods'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Dodongos Cavern Rocks'), lambda state: state.can_blast() or state.has('Progressive Strength Upgrade') or state.is_adult())
    set_rule(world.get_entrance('Dodongos Cavern Lobby'), lambda state: state.can_blast() or state.has('Progressive Strength Upgrade'))
    set_rule(world.get_entrance('Dodongos Cavern Slingshot Target'), lambda state: state.has('Slingshot') or (state.has('Bow') and state.is_adult()))
    set_rule(world.get_entrance('Dodongos Cavern Bomb Drop'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Song from Saria'), lambda state: state.has('Zeldas Letter'))
    set_rule(world.get_entrance('Mountain Summit Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Mountain Summit Fairy Reward'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Hyrule Castle Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Hyrule Castle Fairy Reward'), lambda state: state.has('Zeldas Lullaby') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Ganons Castle Grounds'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Lost Woods Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zora River Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Lake Hylia Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zoras Domain Dive Warp'), lambda state: state.can_dive())
    set_rule(world.get_entrance('Zora River Waterfall'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Zora River Rocks'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Underwater Bottle'), lambda state: state.can_dive())
    set_rule(world.get_location('King Zora Moves'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Behind King Zora'), lambda state: state.has('Bottle with Letter'))
    set_rule(world.get_entrance('Zora River Adult'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Zoras Domain Adult Access'), lambda state: state.has('Zeldas Lullaby'))
    set_rule(world.get_entrance('Zoras Fountain Adult Access'), lambda state: state.can_reach('Zoras Fountain'))
    set_rule(world.get_entrance('Jabu Jabus Belly'), lambda state: state.has('Bottle'))
    set_rule(world.get_entrance('Zoras Fountain Fairy'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Zoras Fountain Fairy Reward'), lambda state: state.has('Zeldas Lullaby') and state.has('Magic Meter'))
    set_rule(world.get_entrance('Jabu Jabus Belly Ceiling Switch'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang'))
    set_rule(world.get_entrance('Jabu Jabus Belly Tentacles'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('Ice Cavern Map Chest'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('Ice Cavern Compass Chest'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('Ice Cavern Iron Boots Chest'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))
    set_rule(world.get_location('Song from Ocarina of Time'), lambda state: state.has('Kokiri Emerald') and state.has('Goron Ruby') and state.has('Zora Sapphire'))
    set_rule(world.get_entrance('Door of Time'), lambda state: state.has('Song of Time'))
    set_rule(world.get_entrance('Adult Forest Warp Pad'), lambda state: state.has('Minuet of Forest') and state.is_adult())
    set_rule(world.get_entrance('Child Forest Warp Pad'), lambda state: state.has('Minuet of Forest'))
    set_rule(world.get_entrance('Adult Meadow Access'), lambda state: state.has('Sarias Song') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Entrance'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Song of Time Block'), lambda state: state.has('Song of Time'))
    set_rule(world.get_entrance('Forest Temple Lobby Eyeball Switch'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Lobby Locked Door'), lambda state: state.has('Progressive Strength Upgrade') and state.has('Small Key (Forest Temple)', 1))
    set_rule(world.get_entrance('Forest Temple Well Connection'), lambda state: (state.has('Iron Boots') and state.is_adult()) or state.has('Progressive Scale', 2))
    set_rule(world.get_entrance('Forest Temple Scarecrows Song'), lambda state: False) #For some reason you can't actually activate this from below. Cool game.
    set_rule(world.get_entrance('Forest Temple Elevator'), lambda state: state.has('Bow') and state.is_adult() and state.has('Progressive Strength Upgrade') and state.has('Small Key (Forest Temple)', 3))
    set_rule(world.get_entrance('Forest Temple Outside Backdoor'), lambda state: state.has('Hover Boots') and state.is_adult())
    set_rule(world.get_entrance('Forest Temple Twisted Hall'), lambda state: state.has('Small Key (Forest Temple)', 3))
    set_rule(world.get_entrance('Forest Temple Straightened Hall'), lambda state: state.has('Small Key (Forest Temple)', 2) and state.has('Bow'))
    set_rule(world.get_entrance('Forest Temple Drop to Falling Room'), lambda state: state.has('Small Key (Forest Temple)', 5) and state.has('Bow'))
    set_rule(world.get_location('Forest Temple Red Poe Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Forest Temple Blue Poe Chest'), lambda state: state.has('Bow') and state.is_adult())
    set_rule(world.get_location('Phantom Ganon'), lambda state: state.has('Boss Key (Forest Temple)'))
    set_rule(world.get_entrance('Dampes Grave'), lambda state: state.is_adult())
    set_rule(world.get_location('Song at Windmill'), lambda state: state.is_adult())
    set_rule(world.get_entrance('Temple Warp Pad'), lambda state: state.has('Prelude of Light'))
    set_rule(world.get_location('Sheik at Temple'), lambda state: state.has('Forest Medallion') and state.is_adult())
    set_rule(world.get_location('Diving in the Lab'), lambda state: state.has('Progressive Scale', 2))
    set_rule(world.get_location('Child Fishing'), lambda state: state.has('Kokiri Sword'))
    set_rule(world.get_location('Adult Fishing'), lambda state: state.is_adult and (state.has('Progressive Hookshot') or state.has('Magic Bean')))
    set_rule(world.get_entrance('Crater Hover Boots'), lambda state: state.is_adult() and state.has('Hover Boots'))
    set_rule(world.get_entrance('Crater Ascent'), lambda state: state.is_adult() and state.has('Goron Tunic') and (state.has('Hover Boots') or state.has('Hammer')))
    set_rule(world.get_entrance('Crater Scarecrow'), lambda state: state.is_adult() and state.has('Progressive Hookshot', 2) and state.has('Goron Tunic'))
    set_rule(world.get_entrance('Crater Bridge'), lambda state: state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot')))
    set_rule(world.get_entrance('Crater Bridge Reverse'), lambda state: state.is_adult() and (state.has('Hover Boots') or state.has('Progressive Hookshot')))
    set_rule(world.get_entrance('Crater Warp Pad'), lambda state: state.has('Bolero of Fire'))
    set_rule(world.get_entrance('Crater Fairy'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_entrance('Fire Temple Entrance'), lambda state: state.is_adult() and state.has('Goron Tunic'))
    set_rule(world.get_entrance('Fire Temple Early Climb'), lambda state: state.has('Small Key (Fire Temple)', 3) and state.has('Progressive Strength Upgrade') and (state.has('Bomb Bag') or ((state.has('Bow') or state.has('Progressive Hookshot')) and state.is_adult())))
    set_rule(world.get_entrance('Fire Temple Fire Maze Escape'), lambda state: state.has('Small Key (Fire Temple)', 7) or (state.has('Small Key (Fire Temple)', 6) and state.has('Hover Boots') and state.has('Hammer') and state.is_adult()))
    set_rule(world.get_location('Fire Temple Fire Dancer Chest'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_location('Fire Temple Boss Key Chest'), lambda state: state.is_adult() and state.has('Hammer'))
    set_rule(world.get_location('Fire Temple Big Lava Room Bombable Chest'), lambda state: state.has('Small Key (Fire Temple)', 1) and state.has('Bomb Bag'))
    set_rule(world.get_location('Fire Temple Big Lava Room Open Chest'), lambda state: state.has('Small Key (Fire Temple)', 1))
    set_rule(world.get_location('Fire Temple Map Chest'), lambda state: state.has('Small Key (Fire Temple)', 5) or (state.has('Small Key (Fire Temple)', 4) and state.is_adult() and state.has('Bow')))
    set_rule(world.get_location('Fire Temple Boulder Maze Upper Chest'), lambda state: state.has('Small Key (Fire Temple)', 5))
    set_rule(world.get_location('Fire Temple Boulder Maze Bombable Pit'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Bomb Bag'))
    set_rule(world.get_location('Fire Temple Scarecrow Chest'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('Fire Temple Compass Chest'), lambda state: state.has('Small Key (Fire Temple)', 6))
    set_rule(world.get_location('Fire Temple Highest Goron Chest'), lambda state: state.has('Song of Time') and state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('Fire Temple Megaton Hammer Chest'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('Volvagia'), lambda state: state.has('Hammer') and state.is_adult() and state.has('Boss Key (Fire Temple)') and (state.has('Hover Boots') or (state.can_reach('Fire Temple Upper') and (state.has('Song of Time') or state.has('Bomb Bag')))))
    set_rule(world.get_location('Sheik in Crater'), lambda state: state.is_adult())
    set_rule(world.get_location('Link the Goron'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag')))
    set_rule(world.get_entrance('Crater Access'), lambda state: state.is_adult() and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag')))
    set_rule(world.get_entrance('Forest Generic Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Forest Sales Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Front of Meadow Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Remote Southern Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Near Lake Inside Fence Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Valley Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Far West Castle Town Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field Kakariko Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Field North Lon Lon Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Castle Storms Grotto'), lambda state: state.has('Song of Storms'))
    set_rule(world.get_entrance('Kakariko Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Mountain Bombable Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Top of Crater Grotto'), lambda state: state.can_blast())
    set_rule(world.get_entrance('Zora River Plateau Bombable Grotto'), lambda state: state.can_blast())

    set_rule(world.get_location('GS2'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('GS3'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS4'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('GS5'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('GS6'), lambda state: state.has('Magic Bean'))
    set_rule(world.get_location('GS7'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS9'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang') or (state.has('Dins Fire') and state.has('Magic Meter')))
    set_rule(world.get_location('GS11'), lambda state: state.has('Boomerang') and state.has('Bomb Bag'))
    set_rule(world.get_location('GS12'), lambda state: state.has('Boomerang') or (state.has('Progressive Hookshot') and state.is_adult()))
    set_rule(world.get_location('GS13'), lambda state: (state.has('Hammer') and state.has_fire_source() and state.has('Progressive Hookshot') and state.is_adult()) or (state.has('Boomerang') and state.has('Bomb Bag') and state.has('Dins Fire') and state.has('Magic Meter')))
    set_rule(world.get_location('GS16'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS20'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS21'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS26'), lambda state: state.has('Slingshot') or state.has('Bomb Bag'))
    set_rule(world.get_location('GS27'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS28'), lambda state: state.has('Boomerang'))
    set_rule(world.get_location('GS29'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('GS30'), lambda state: state.has('Bottle') and (state.has('Bomb Bag') or state.has('Progressive Strength Upgrade')))
    set_rule(world.get_location('GS31'), lambda state: state.can_blast())
    set_rule(world.get_location('GS32'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS33'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS34'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('GS35'), lambda state: state.is_adult())
    set_rule(world.get_location('GS37'), lambda state: state.has('Bolero of Fire') and state.has('Bottle'))
    set_rule(world.get_location('GS39'), lambda state: state.has('Slingshot') or state.has('Bomb Bag') or state.has('Boomerang') or (state.has('Dins Fire') and state.has('Magic Meter')) or (state.is_adult and (state.has('Progressive Hookshot') or state.has('Bow')))) #Biggoron Sword also works, outside of logic for now
    set_rule(world.get_location('GS41'), lambda state: (state.has('Progressive Hookshot') and state.is_adult()) or state.has('Boomerang'))
    set_rule(world.get_location('GS42'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS45'), lambda state: (state.has('Progressive Hookshot') and state.has('Magic Bean')) or state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('GS46'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS47'), lambda state: state.has('Progressive Hookshot') or state.has('Bow') or state.has('Magic Meter'))
    set_rule(world.get_location('GS49'), lambda state: state.has('Boomerang'))
#    set_rule(world.get_location('GS50'), lambda state: state.has('Progressive Strength Upgrade', 2) and state.can_blast() and state.has('Progressive Hookshot'))
# Jabu Jabu GS need no reqs becuase the access reqs for their zones cover them.
    set_rule(world.get_location('GS55'), lambda state: state.has('Bottle'))
    set_rule(world.get_location('GS56'), lambda state: state.has('Boomerang'))
#    set_rule(world.get_location('GS58'), lambda state: state.is_adult() and state.has('Progressive Hookshot', 2))
    set_rule(world.get_location('GS59'), lambda state: state.is_adult() and state.has('Iron Boots') and state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS60'), lambda state: (state.has('Progressive Hookshot') or state.has('Bow') or (state.has('Dins Fire') and state.has('Magic Meter'))) and state.is_adult())
    set_rule(world.get_location('GS61'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS62'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS63'), lambda state: (state.has('Progressive Hookshot', 2) or (state.has('Progressive Hookshot') and state.can_reach('Forest Temple Outside Upper Ledge'))) and state.is_adult())
    set_rule(world.get_location('GS64'), lambda state: state.has('Progressive Hookshot'))
    set_rule(world.get_location('GS65'), lambda state: state.has('Small Key (Fire Temple)', 1) and state.has('Song of Time'))
    set_rule(world.get_location('GS66'), lambda state: state.has('Bomb Bag'))
    set_rule(world.get_location('GS67'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS68'), lambda state: state.has('Small Key (Fire Temple)', 5) and state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS69'), lambda state: state.has('Hammer') and state.is_adult())
    set_rule(world.get_location('GS70'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS71'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS72'), lambda state: state.has('Progressive Hookshot') and state.is_adult())
    set_rule(world.get_location('GS78'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang') and (state.has('Progressive Strength Upgrade') or state.has('Bomb Bag') or (state.has('Lens of Truth') and state.has('Magic Meter'))))
    set_rule(world.get_location('GS79'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang'))
    set_rule(world.get_location('GS80'), lambda state: state.has('Small Key (Bottom of the Well)', 2) and state.has('Boomerang'))