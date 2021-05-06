import xml.etree.ElementTree as ET
from pprint import pprint
import os
import re
from inc.all_sg_keys import all_spawn_keys


def import_spawngroups(search_dir, debug=False):

    # =======================================================================================
    # Import data about MES and RAI tags from required files
    # =======================================================================================

    keys_to_report_on = [
        'FactionOwner',
        'SpaceCargoShip',
        'SpaceRandomEncounter',
        'LunarCargoShip',
        'AtmosphericCargoShip',
        'PlanetaryInstallation'
    ]

    with open(r'report_keys.txt', 'r') as report_keys_file:
        for a_key in report_keys_file.readlines():
            if len(a_key) > 0 and not a_key.startswith('#') and not a_key == 'FactionOwner':
                keys_to_report_on.append(a_key.strip())

    if debug:
        print('Imported Keys:')
        for this_key in keys_to_report_on:
            print(f'    {this_key}')
        print('\n')

    # =======================================================================================
    # Get a list of absolute paths to .sbc files in the defined directory
    # =======================================================================================

    get_walk = os.walk(f'{search_dir}')

    sbc_paths = []

    for wdir, dirs, files in get_walk:
        wdir = wdir.replace("\\", "/")
        for a_file in files:
            if a_file.endswith('.sbc'):
                a_file = a_file.replace("\\", "/")
                sbc_paths.append(f'{wdir}/{a_file}')
    if debug:
        pprint(sbc_paths)

    # =======================================================================================
    # Initialize variables for summary
    # =======================================================================================

    files_found = len(sbc_paths)
    files_checked = 0
    spawn_groups_checked = 0
    spawn_groups_reported = 0

    # =======================================================================================
    # Analyze each file, one at a time, and extract spawngroup information
    # =======================================================================================

    all_sg = {}

    for each_file in sbc_paths:
        files_checked += 1

        tree = ET.parse(each_file)
        root = tree.getroot()

        if debug:
            print(root)

        just_sgs = ET.ElementTree(root).iter('SpawnGroup')

        for this_sg in just_sgs:
            spawn_groups_checked += 1

            this_key = ''
            this_data = {
                'SubtypeId': '',
                'IsPirate': '',
                'Frequency': '',
                'FactionOwner': 'none',
                'Prefabs': [],
            }

            prefab_index = -1

            for this_key in keys_to_report_on:
                this_data[this_key] = all_spawn_keys[this_key]['default']

            current_prefab = ''
            try_this = ET.ElementTree(this_sg).iter()
            for a_thing in try_this:
                if debug:
                    print(f'>>"{a_thing.tag:>24} : {a_thing.text}"')
                if a_thing.tag == 'SubtypeId':
                    this_data['SubtypeId'] = a_thing.text
                elif a_thing.tag == 'IsPirate':
                    this_data['IsPirate'] = a_thing.text
                elif a_thing.tag == 'Frequency':
                    this_data['Frequency'] = a_thing.text
                elif a_thing.tag == 'Prefab':
                    current_prefab = a_thing.attrib['SubtypeId']
                    # this_data['Prefabs'][current_prefab] = {
                    #     'Prefab': current_prefab,
                    #     'X': '',
                    #     'Y': '',
                    #     'Z': '',
                    #     'Speed': '',
                    #     'Behaviour': ''
                    # }
                    prefab_index = len(this_data['Prefabs'])
                    this_data['Prefabs'].append({
                        'Prefab': current_prefab,
                        'X': '',
                        'Y': '',
                        'Z': '',
                        'Speed': '',
                        'Behaviour': ''
                    })

                elif a_thing.tag == 'X':
                    this_data['Prefabs'][prefab_index]['X'] = a_thing.text
                elif a_thing.tag == 'Y':
                    this_data['Prefabs'][prefab_index]['Y'] = a_thing.text
                elif a_thing.tag == 'Z':
                    this_data['Prefabs'][prefab_index]['Z'] = a_thing.text
                elif a_thing.tag == 'Behaviour':
                    this_data['Prefabs'][prefab_index]['Behaviour'] = a_thing.text
                elif a_thing.tag == 'Speed':
                    this_data['Prefabs'][prefab_index]['Speed'] = a_thing.text
                elif a_thing.tag == 'Description':
                    find_mes_tags = re.compile(r'\[(.*):(.*)]').findall(a_thing.text)
                    for found_tag in find_mes_tags:
                        mes_tag, mes_value = found_tag
                        if mes_tag.strip() in keys_to_report_on:
                            this_data[mes_tag.strip()] = mes_value.strip()

                if len(this_data['SubtypeId']) > 0:
                    all_sg[this_data['SubtypeId']] = this_data

    for each_sg in all_sg:
        if len(each_sg) == 0:
            continue
        triggered_only = 'false'
        if (all_sg[each_sg]['SpaceCargoShip'] == 'false' and
                all_sg[each_sg]['SpaceRandomEncounter'] == 'false' and
                all_sg[each_sg]['LunarCargoShip'] == 'false' and
                all_sg[each_sg]['AtmosphericCargoShip'] == 'false' and
                all_sg[each_sg]['PlanetaryInstallation'] == 'false'):
            all_sg[each_sg]['TriggeredOnly'] = 'true'
        else:
            all_sg[each_sg]['TriggeredOnly'] = 'false'

    if debug:
        pprint(all_sg,  width=160)

    spawn_groups_reported = len(all_sg)

    print(f"""
Output  Summary
---------------
    {files_found:>4} : Files Found 
    {files_checked:>4} : Files Checked 
    {spawn_groups_checked:>4} : Spawn Groups Found
    {spawn_groups_reported:>4} : Spawn Groups Reported
""")

    return {
        'summary': {
            'Files Found': files_found,
            'Files Checked': files_checked,
            'Spawn Groups Found': spawn_groups_checked,
            'Spawn Groups Reported': spawn_groups_reported
        },
        'data': all_sg
    }
