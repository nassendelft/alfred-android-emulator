from subprocess import check_output
from xml.etree import ElementTree
from sys import argv
from os import getenv
from os import path


def get_emulator_executable():
    """
    Reads the 'ANDROID_HOME' environment variable to get to the
    emulator binary path
    """
    android_home_env = getenv('ANDROID_HOME')
    if android_home_env is not None:
        return path.join(path.expandvars(android_home_env), "emulator/emulator")

    raise ValueError("Could not determine emulator executable location")


def build_emulator_item(title):
    item_el = ElementTree.Element('item')
    item_el.attrib = {'arg': title, 'type': 'file'}
    title_el = ElementTree.Element('title')
    title_el.text = title.replace("_", " ")
    item_el.append(title_el)
    return item_el


def weigh_item(item, query):
    """
    Weighs items against given query
    3 - query matches exactly
    2 - items starts with the query
    1 - the query has a partial match
    0 - there's no match
    """
    return 3 if item == query else 2 if item.startswith(query) else 1 if query in item else 0


def search_by_query(items, query):
    """
    Searches for items that matches the query.
    It filters out non matches and sorts it by
    the weigh_item function
    """
    weighed = [(emu, weigh_item(emu, query)) for emu in items]
    filtered = [emu for emu in weighed if emu[1] > 0]
    sorts = sorted(filtered)
    return [emu[0] for emu in sorts]


def build_xml_tree(items):
    root = ElementTree.Element('items')
    for item in [build_emulator_item(element) for element in items]:
        root.append(item)
    return root


emu_path = get_emulator_executable()
emulators = check_output([emu_path, "-list-avds"]).decode("utf-8").rstrip().split('\n')
sorted_items = emulators if len(argv) == 1 else search_by_query(emulators, argv[1])
xml = ElementTree.tostring(build_xml_tree(sorted_items), encoding='utf8', method='xml').decode()
print(xml)
