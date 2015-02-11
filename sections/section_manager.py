__author__ = 'faebser'

manager = dict()


def register_section(name, section):
    manager.update({name: section})


def get_all_sections():
    return manager


def get_all_names():
    return manager.keys()


def get_dicts():
    data = dict()
    for key in manager.iterkeys():
        data.update({
            key: manager[key].to_dict()
        })
    return data
