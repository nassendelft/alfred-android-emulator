from subprocess import check_output
from xml.etree import ElementTree as etree
from sys import argv
from os import getenv
from os import path

path = path.expandvars(getenv('emu_path'))

emulators = check_output([path, "-list-avds"]).decode("utf-8").rstrip().split('\n')


def build_item(title):
    item_el = etree.Element('item')
    item_el.attrib = {'arg': title, 'type': 'file'}
    title_el = etree.Element('title')
    title_el.text = title
    item_el.append(title_el)
    return item_el

root = etree.Element('items')
tree = etree.ElementTree(root)

for emu in emulators:
    if len(argv) == 1 or emu.startswith(argv[1]):
        root.append(build_item(emu))

print(etree.tostring(root, encoding='utf8', method='xml').decode())

