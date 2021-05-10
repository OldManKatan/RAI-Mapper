import xml.etree.ElementTree as ET
from pprint import pprint
import os
import re
import csv
import sys
import signal
from inc.all_sg_keys import all_spawn_keys
import time
import json


def mk_lvl(all_comps, ind, ind_l, a_dict):
    print(f"{' ' * ind * ind_l}|==> {a_dict['name']} ({a_dict['type']})")
    for a_call in a_dict['calls']:
        mk_lvl(all_comps, ind, ind_l + 1, all_comps[a_call])


def import_components(search_dir, debug=False):
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
    comps_checked = 0
    comps_found = 0
    comps_duplicate = 0
    duplicate_data = {}
    errors = []

    # =======================================================================================
    # Analyze each file, one at a time, and extract spawngroup information
    # =======================================================================================

    match_rai_type = re.compile(
        r'\[RivalAI (Action|Autopilot|Behavior|Chat|Command|Condition|Spawn|Target|Trigger|TriggerGroup|Waypoint)\]')
    match_mes_type = re.compile(
        r'\[MES (Dereliction)\]')

    match_action_data = re.compile(r'\[Actions:(\S+)\]')
    match_pri_autopilot_data = re.compile(r'\[AutopilotData:(\S+)\]')
    match_sec_autopilot_data = re.compile(r'\[SecondaryAutopilotData:(\S+)\]')
    match_chat_data = re.compile(r'\[ChatData:(\S+)\]')
    match_command_data = re.compile(r'\[CommandProfileIds:(\S+)\]')
    match_condition_data = re.compile(r'\[Conditions:(\S+)\]')
    match_spawn_data = re.compile(r'\[Spawner:(\S+)\]')
    match_target_data = re.compile(r'\[TargetData:(\S+)\]')
    match_sec_target_data = re.compile(r'\[OverrideTargetData:(\S+)\]')
    match_trigger_data = re.compile(r'\[Triggers:(\S+)\]')
    match_triggergroup_data = re.compile(r'\[TriggerGroups:(\S+)\]')
    match_waypoint_data = re.compile(r'\[Waypoint:(\S+)\]')

    matches = [
        match_action_data,
        match_pri_autopilot_data,
        match_sec_autopilot_data,
        match_chat_data,
        match_command_data,
        match_condition_data,
        match_spawn_data,
        match_target_data,
        match_sec_target_data,
        match_trigger_data,
        match_triggergroup_data,
        match_waypoint_data
    ]

    all_comps = {}
    name_to_key = {}
    pri_key = 0

    for each_file in sbc_paths:
        files_checked += 1

        try:
            tree = ET.parse(each_file)
            root = tree.getroot()
        except ET.ParseError as e:
            error_text = f"Issue detected with file {each_file}:\n    {type(e)}: {e}"
            print(error_text)
            errors.append(error_text)
            continue

        if debug:
            print(root)

        just_comps = ET.ElementTree(root).iter('EntityComponent')

        for this_comp in just_comps:
            comp_type = None
            iter_tags = ET.ElementTree(this_comp).iter()
            for a_thing in iter_tags:
                if a_thing.tag == 'Description':
                    if a_thing.text.find('[RivalAI ') != -1:
                        comp_type = 'rai'
                    elif a_thing.text.find('[MES ') != -1 or a_thing.text.find('[Modular Encounters ') != -1:
                        comp_type = 'mes'

            comps_checked += 1

            if not comp_type:
                continue

            this_data = {
                'key': 0,
                'name': '',
                'type': '',
                'desc': '',
                'file': each_file.replace('\\', '/').split('/')[-1],
                'calls': [],
                'noexist': [],
                'comp_type': comp_type
            }

            iter_tags = ET.ElementTree(this_comp).iter()
            for a_thing in iter_tags:
                if a_thing.tag == 'SubtypeId':
                    this_data['name'] = a_thing.text
                elif a_thing.tag == 'Description':
                    this_data['desc'] = a_thing.text

            has_type = None
            find_type = match_rai_type.findall(this_data['desc'])
            if find_type:
                has_type = find_type[0]
            find_type = match_mes_type.findall(this_data['desc'])
            if find_type:
                has_type = find_type[0]

            if has_type:
                if this_data['name'] not in name_to_key:
                    comps_found += 1
                    this_data['type'] = has_type
                    this_data['key'] = pri_key
                    pri_key += 1

                    all_comps[this_data['key']] = this_data
                    name_to_key[this_data['name']] = this_data['key']
                else:
                    comps_duplicate += 1
                    if this_data['name'] not in duplicate_data:
                        duplicate_data[this_data['name']] = []
                        duplicate_data[this_data['name']].append(all_comps[name_to_key[this_data['name']]]['file'])
                    duplicate_data[this_data['name']].append(this_data['file'])

    # =======================================================================================
    # Write the results out to screen
    # =======================================================================================

    is_not_called = []
    is_called = []
    if debug:
        print('{')
    for a_key in all_comps:
        is_not_called.append(a_key)
        this_dict = all_comps[a_key]
        if debug:
            print(f'    {a_key:>3} : {{')
            for each_key in this_dict:
                print(f'        {each_key:>8} : {this_dict[each_key]},')
            print('    },')

    for a_key in all_comps:
        this_dict = all_comps[a_key]
        for a_match in matches:
            find_this = a_match.findall(this_dict['desc'])
            if find_this:
                for each_found in find_this:
                    if each_found in name_to_key:
                        this_key = name_to_key[each_found]
                        this_dict['calls'].append(this_key)
                        if this_key in is_not_called:
                            is_not_called.remove(this_key)
                        if this_key not in is_called:
                            is_called.append(this_key)
                    else:
                        this_dict['noexist'].append(each_found)

    print(f"\n\n==== COMPONENT HIERARCHY ====")
    never_called = []
    indent = 4
    indent_lvl = 1
    for a_key in is_not_called:
        td = all_comps[a_key]
        if td['type'] == 'Behavior':
            print(f"{td['name']} ({td['type']})")
            for a_call in td['calls']:
                mk_lvl(all_comps, indent, indent_lvl, all_comps[a_call])
        else:
            never_called.append(td['name'])

    print(f"\n\n==== UNUSED COMPONENTS ====")
    unused_output_list = []
    for thing in never_called:
        unused_string = f"{thing:<48} File: {all_comps[name_to_key[thing]]['file']}"
        print(unused_string)
        unused_output_list.append([thing, f"File: {all_comps[name_to_key[thing]]['file']}"])

    print(f"\n\n==== COMPONENT DOES NOT EXIST ====")
    comp_noexist_list = []
    for a_key in all_comps:
        for noex in all_comps[a_key]['noexist']:
            comp_noexist_str = f"{noex} is called by {all_comps[a_key]['name']} in file {all_comps[a_key]['file']}"
            print(comp_noexist_str)
            comp_noexist_list.append(comp_noexist_str)

    print(f"\n\n==== DUPLICATES ====")
    dup_data_dict = {}
    if duplicate_data:
        for a_comp in duplicate_data:
            dup_data_dict[a_comp] = []
            print(f'{a_comp} show up in these files:')
            for a_file in duplicate_data[a_comp]:
                print(f'    {a_file}')
                dup_data_dict[a_comp].append(a_file)
    else:
        print('None')

    print(f"\n\n==== FILE ERRORS ====")
    if errors:
        print('\n'.join(errors))
    else:
        print('None')

    print(f"""
Output  Summary
---------------
    {files_found:>4} : Files Found
    {files_checked:>4} : Files Checked
    {comps_checked:>4} : Components Checked
    {comps_found:>4} : Components Found
    {len(is_not_called):>4} : Top level Components
    {len(is_called):>4} : Used Components
    {len(never_called):>4} : Unused Components
    {comps_duplicate:>4} : Duplicate Definitions
    {len(errors):>4} : File Errors
""")

    return {
        'summary': {
            'Files Found': files_found,
            'Files Checked': files_checked,
            'Components Checked': comps_checked,
            'Components Found': comps_found,
            'Top level Components': len(is_not_called),
            'Used Components': len(is_called),
            'Unused Components': len(never_called),
            'Duplicate Definitions': comps_duplicate,
            'File Errors': len(errors)
        },
        'detail': {
            'unused_comps': unused_output_list,
            'noexist_comps': comp_noexist_list,
            'duplicate_data': dup_data_dict,
            'file_errors': errors
        },
        'data': all_comps
    }
