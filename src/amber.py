"""
This file contains all general operations
"""

import pdb
class db(dict):

    def __getitem__(self, item):
        pdb.set_trace()
        return super().__getitem__(item)

database ={}


class AmberObject(object):

    """
    Base class for all objects on the network
    """

    current_available_id = 0

    @staticmethod
    def get_item(id):
        if id in database:
            return database[id]

    def __init__(self, new_object):
        if new_object:
            self.id = str(AmberObject.current_available_id)
            AmberObject.current_available_id += 1
            database[self.id] = self
        else:
            self.id = None

    @staticmethod
    def __getitem__(id):
        return AmberObject.get_item(id)

    @staticmethod
    def __delitem__(id):
        if id in database:
            del database[id]


import personal_docks
import seas
import ships


def is_personal_dock(in_object):
    return type(in_object) is personal_docks.PersonalDock


def generate_personal_docks():
    for member_id, member in database.items():
        if is_personal_dock(member):
            yield member_id


def most_friends_members_generator():
    members_id = generate_personal_docks()
    sorted_members = sorted(members_id, key=lambda id: len(database[id].friends), reverse=True)
    for member_id in sorted_members:
        yield member_id, len(database[member_id].friends)


def most_followers_members_generator():
    members_id = generate_personal_docks()
    sorted_members = sorted(members_id, key=lambda id: len(database[id].followers), reverse=True)
    for member_id in sorted_members:
        yield member_id, len(database[member_id].followers)


def most_posts_members_generator():
    members_id = generate_personal_docks()
    sorted_members = sorted(members_id, key=lambda id: len(database[id].sailed_ships), reverse=True)
    for member_id in sorted_members:
        yield member_id, len(database[member_id].sailed_ships)


def max_reactions_ship_for_each_member_generator():
    for member_id in generate_personal_docks():
        yield member_id, database[member_id].max_reactions_ship()


def max_comments_ship_for_each_member_generator():
    for member_id in generate_personal_docks():
        yield member_id, database[member_id].max_comments_ship()


def is_sea(in_object):
    return type(in_object) is seas.Sea


def generate_seas():
    for sea_id, sea in database.items():
        if is_sea(sea):
            yield sea_id


def most_members_seas_generator():
    groups_id = generate_seas()
    sorted_groups = sorted(groups_id, key=lambda id: len(database[id].members), reverse=True)
    for group_id in sorted_groups:
        yield group_id, len(database[group_id].members)


def most_posts_seas_generator():
    groups_id = generate_seas()
    sorted_groups = sorted(groups_id, key=lambda id: len(database[id].sailed_ships), reverse=True)
    for group_id in sorted_groups:
        yield group_id, len(database[group_id].sailed_ships)


def max_reactions_ship_for_each_sea_generator():
    for group_id in generate_seas():
        yield group_id, database[group_id].max_reactions_ship()


def max_comments_ship_for_each_sea_generator():
    for group_id in generate_seas():
        yield group_id, database[group_id].max_comments_ship()


def is_ship(in_object):
    return type(in_object) is ships.Ship


def generate_ships():
    for ship_id, ship in database.items():
        if is_ship(ship):
            yield ship_id


def export_database():
    file = open('database.db', 'w')
    file.write(str(AmberObject.current_available_id))
    file.write('++|++')
    for value in database.values():
        file.write(str(value.id))
        file.write('+|+')
        file.write(value.export_to_database())
        file.write('+|+')
        file.write(str(type(value)))
        file.write('++|++')
    file.close()


def import_database():
    file = open('database.db', 'r')
    f_data = file.read().split('++|++')
    AmberObject.current_available_id = int(f_data[0])
    del f_data[0]
    del f_data[len(f_data) - 1]
    for object in f_data:
        id, in_data, in_type = object.split('+|+')
        if in_type == "<class 'personal_docks.PersonalDock'>":
            database[id] = personal_docks.PersonalDock.import_from_database(in_data)
            database[id].id = id
        elif in_type == "<class 'seas.Sea'>":
            database[id] = seas.Sea.import_from_database(in_data)
            database[id].id = id
        elif in_type == "<class 'ships.Ship'>":
            database[id] = ships.Ship.import_from_database(in_data)
            database[id].id = id
    file.close()
