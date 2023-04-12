from django import template
from django.shortcuts import render
from django.template import loader
from .. import models
from typing import List, Dict, Optional


register = template.Library()


@register.filter
def get_item(dictionary: dict, key):
    return dictionary.get(key)


def get_entries(menu_id: int) -> List[models.Entry]:
    entries = models.Entry.objects.raw(
        'WITH RECURSIVE entries(id, name, parent_id, menu_id) AS (\n'
        'SELECT id, name, parent_id, menu_id\n'
        'FROM test_app_entry\n'
        f'WHERE menu_id = {menu_id} AND parent_id IS NULL\n'
        ' UNION ALL\n'
        'SELECT t.id, t.name, t.parent_id, t.menu_id\n'
        'FROM test_app_entry AS t, entries AS e\n'
        'WHERE e.id = t.parent_id\n'
        ')\n'
        'SELECT * FROM entries as ee\n'
        'ORDER BY ee.id\n'
    )
    return [e for e in entries]


def to_tree(entries: List[models.Entry]) -> Dict[int, List[models.Entry]]:
    res = dict()  # preservers order
    for entry in entries:
        if entry.parent and entry.parent.id in res:
            res[entry.parent.id].append(entry)
        res[entry.id] = []
    return res


def handle_chosen_id(chosen_id: Optional[int], entries: List[models.Entry]) -> Optional[int]:
    if chosen_id is not None:
        return chosen_id
    if entries:
        return entries[0].id
    return None  # It's possible to have not even one entry in the DB


@register.inclusion_tag('menu.html')
def draw_menu(menu_id: int, chosen_id: Optional[int] = None) -> dict:
    entries = get_entries(menu_id)
    tree = to_tree(entries)
    menu = models.Menu.objects.get(id=menu_id)

    return {
        'menu_id': menu_id,
        'menu_name': menu.name,
        'tree': tree,
        'entries': filter(lambda x: not x.parent, entries),
        'chosen_id': handle_chosen_id(chosen_id, entries)
    }
