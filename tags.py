from keyword import iskeyword
__tags = """
armor
protection
cover
physical_damage
structure
elemental_composition
blood_level
movement_speed
"""
__triggers = """
turn
"""
for index, name in enumerate(__tags.split('\n')):
    if not name:
        continue
    if iskeyword(name) or not name.isidentifier():
        raise ValueError('Invalid tag name - `' + name + '`')
    globals()[name] = index
for index, name in enumerate(__triggers.split('\n')):
    if not name:
        continue
    if iskeyword(name) or not name.isidentifier():
        raise ValueError('Invalid tag name')
    globals()[name+'_action'] = index
print('\n'.join(filter(lambda x: not x.startswith('_'), globals())))


