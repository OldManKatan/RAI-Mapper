import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import json
from inc.import_spawngroups import import_spawngroups
from inc.import_components import import_components


def check_threat(new_value):
    for a_char in new_value:
        if a_char not in ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return False
    return True


class RAIMapper:
    def __init__(self, root):
        self.parent_file_path = ''
        self.spawngroup_dict = {}
        self.component_dict = {}

        self.player_threat_value = tk.IntVar()
        self.player_threat_value.set(-1)
        self.include_non_triggeredonly = tk.IntVar()
        self.include_non_triggeredonly.set(1)
        self.include_triggeredonly = tk.IntVar()
        self.include_triggeredonly.set(1)
        self.include_sre = tk.IntVar()
        self.include_sre.set(1)
        self.include_scs = tk.IntVar()
        self.include_scs.set(1)

        self.debug = False

        self.root = root
        self.chk_thr = self.root.register(check_threat)

        self.style = ttk.Style()

        self.style.theme_create(
            "raim_theme", parent="alt", settings={
                ".": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#C3C3C3",
                        "relief": "flat",
                        "font": ('Arial', 12),
                        "borderwidth": 0
                    }
                },
                "TCheckButton": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#000000"
                    }
                },
                "TFrame": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#C3C3C3",
                        "padding": 10,
                        "margin": 0
                    }
                },
                "TLabel": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#C3C3C3",
                        "padding": 2
                    }
                },
                "Header.TLabel": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#C3C3C3",
                        "font": ('Arial', 16),
                        "padding": 10
                    }
                },
                "TNotebook": {
                    "configure": {
                        "tabmargins": [2, 5, 2, 0]
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "darkcolor": "#303030",
                        "lightcolor": "#303030",
                        "padding": [10, 3],
                        "background": "#4260d6",
                        "foreground": "#C3C3C3",
                        "font": ('Arial', 16)
                    },
                    "map": {
                        "background": [("selected", "#7290f6")],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                },
                "TScrollbar": {
                    "configure": {
                        "arrowcolor": "#303030",
                        "background": "#C3C3C3",
                        "foreground ": "#C3C3C3",
                        "troughcolor": "#303030"
                    }
                },
                "Treeview": {
                    "configure": {
                        "bordercolor": "#303030",
                        "darkcolor": "#303030",
                        "lightcolor": "#C3C3C3",
                        "padding": [5, 1],
                        "background": "#303030",
                        "fieldbackground": "#303030",
                        "font": ('Arial', 12)
                    },
                    "map": {
                        "background": [("selected", "#303030")],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                }
            }
        )

        self.style.theme_use("raim_theme")

        self.f_main = ttk.Frame(self.root)

        self.l_lm_title = ttk.Label(
            self.f_main, text="Menu", font=('Arial', 20, 'bold'), anchor=tk.CENTER)
        self.l_lm_title.grid(row=0, column=0, padx=5, pady=20, sticky='ew')

        self.b_lm_load = tk.Button(
            self.f_main,
            text="Load",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.import_from_sbc
        )
        self.b_lm_load.grid(row=1, column=0, padx=5, pady=2, sticky='ew')

        self.sep_lm_sep1 = ttk.Separator(self.f_main)
        self.sep_lm_sep1.grid(row=2, column=0, padx=10, pady=7, sticky='ew')

        self.b_lm_exp_csv = tk.Button(
            self.f_main,
            text="Export CSV",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.export_to_csv,
            state="disabled"
        )
        self.b_lm_exp_csv.grid(row=3, column=0, padx=5, pady=2, sticky='ew')

        self.b_lm_exp_json = tk.Button(
            self.f_main,
            text="Export JSON",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.export_to_json,
            state="disabled"
        )
        self.b_lm_exp_json.grid(row=4, column=0, padx=5, pady=2, sticky='ew')

        self.sep_lm_sep50 = ttk.Separator(self.f_main)
        self.sep_lm_sep50.grid(row=50, column=0, padx=10, pady=7, sticky='ew')

        self.b_lm_quit = tk.Button(
            self.f_main,
            text="Quit",
            relief="flat",
            background="#ab2626",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.root.destroy
        )
        self.b_lm_quit.grid(row=99, column=0, padx=5, pady=2, sticky='ew')

        self.sep_lm_sepright = ttk.Separator(self.f_main, orient=tk.VERTICAL)
        self.sep_lm_sepright.grid(row=0, column=1, rowspan=99, padx=5, pady=5, sticky='ns')

        self.tabs = ttk.Notebook(self.f_main)

        self.summ_tab = ttk.Frame(self.tabs)
        self.summ_tab.grid_columnconfigure(0, weight=1)
        self.summ_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.summ_tab, text='Summary')

        self.det_tab = ttk.Frame(self.tabs)
        self.det_tab.grid_columnconfigure(0, weight=1)
        self.det_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.det_tab, text='Details')

        self.sg_tab = ttk.Frame(self.tabs)
        self.sg_tab.grid_columnconfigure(0, weight=1)
        self.sg_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.sg_tab, text='Spawn Groups')

        self.comp_tab = ttk.Frame(self.tabs)
        self.comp_tab.grid_columnconfigure(0, weight=1)
        self.comp_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.comp_tab, text='RAI Components')

        self.threat_tab = ttk.Frame(self.tabs)
        self.threat_tab.grid_columnconfigure(0, weight=1)
        self.threat_tab.grid_rowconfigure(1, weight=1)

        self.tabs.add(self.threat_tab, text='SG by Threat')

        self.summ_frame = ttk.Frame(self.summ_tab)
        self.summ_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.l_summ_nodata = ttk.Label(
            self.summ_frame,
            text='No data loaded.\n',
            style='Header.TLabel'
        )
        self.l_summ_nodata.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        self.l_summ_nodata2 = ttk.Label(
            self.summ_frame,
            text='Use the "Load" button on the top left to load your mod.\n'
            'Select the parent directory of your MES mod\'s "data" directory.'
        )
        self.l_summ_nodata2.grid(row=1, column=0, padx=5, pady=5, sticky='nw')

        self.det_frame = ttk.Frame(self.det_tab)
        self.det_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.det_frame.grid_columnconfigure(1, weight=1)
        self.det_frame.grid_rowconfigure(98, weight=1)

        self.l_det_nodata = ttk.Label(
            self.det_frame,
            text='No data loaded.\n',
            style='Header.TLabel'
        )
        self.l_det_nodata.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        self.sg_tree = ttk.Treeview(self.sg_tab)
        self.sg_tree["columns"] = ["Triggered", "Faction", "SpaceRandomEncounter", "SpaceCargoShip"]
        self.sg_tree.column("#0", width=350, stretch=False)
        self.sg_tree.heading("#0", text="SpawnGroup")
        for a_col in self.sg_tree["columns"]:
            self.sg_tree.column(a_col, width=50)
            self.sg_tree.heading(a_col, text=a_col)
        self.sg_tree.insert("", 1, "", text="No data loaded...", values=(""))

        self.sg_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.sg_tree_yscroll = ttk.Scrollbar(
            self.sg_tab, orient='vertical', command=self.sg_tree.yview)
        self.sg_tree.configure(yscrollcommand=self.sg_tree_yscroll.set)
        self.sg_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

        self.comp_tree = ttk.Treeview(self.comp_tab)
        self.comp_tree["columns"] = "type"
        self.comp_tree.column("#0", width=500, stretch=False)
        self.comp_tree.column("type", width=100)
        self.comp_tree.heading("#0", text="SubTypeId")
        self.comp_tree.heading("type", text="Type")
        self.comp_tree.insert("", 1, "", text="No data loaded...", values=(""))
        self.comp_tree.bind('<<TreeviewOpen>>', self.handle_open_event)

        self.comp_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.comp_tree_yscroll = ttk.Scrollbar(
            self.comp_tab, orient='vertical', command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=self.comp_tree_yscroll.set)
        self.comp_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

        self.threat_select_frame = ttk.Frame(self.threat_tab)
        self.threat_select_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.threat_select_frame.grid_columnconfigure(3, weight=1)
        self.threat_select_frame.grid_rowconfigure(98, weight=1)

        self.th_l_min_threat = ttk.Label(self.threat_select_frame, text="Player threat")
        self.th_l_min_threat.grid(row=0, column=0, padx=10, pady=3, sticky='ew')
        self.th_e_min_threat = ttk.Entry(
            self.threat_select_frame,
            font=("Calibri", 12),
            textvariable=self.player_threat_value,
            validate='key',
            validatecommand=(self.chk_thr, '%P')
        )
        self.th_e_min_threat.grid(row=0, column=1, padx=10, pady=3, sticky='ew')

        self.th_b_get_sg = tk.Button(
            self.threat_select_frame,
            text="Get SpawnGroups",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.get_threat_sgs
        )
        self.th_b_get_sg.grid(row=2, column=0, padx=10, pady=3, sticky='ew', rowspan=2, columnspan=2)

        self.th_l_inc_notrig = ttk.Label(self.threat_select_frame, text="Include Spawned Encounters")
        self.th_l_inc_notrig.grid(row=0, column=2, padx=10, pady=3, sticky='ew')
        self.th_ch_inc_notrig = ttk.Checkbutton(self.threat_select_frame, variable=self.include_non_triggeredonly)
        self.th_ch_inc_notrig.grid(row=0, column=3, padx=10, pady=3, sticky='ew')
        self.th_l_inc_trig = ttk.Label(self.threat_select_frame, text="Include Triggered-Only Encounters")
        self.th_l_inc_trig.grid(row=1, column=2, padx=10, pady=3, sticky='ew')
        self.th_ch_inc_trig = ttk.Checkbutton(self.threat_select_frame, variable=self.include_triggeredonly)
        self.th_ch_inc_trig.grid(row=1, column=3, padx=10, pady=3, sticky='ew')

        self.th_l_inc_sre = ttk.Label(self.threat_select_frame, text="Include SpaceRandomEncounters")
        self.th_l_inc_sre.grid(row=2, column=2, padx=10, pady=3, sticky='ew')
        self.th_ch_inc_sre = ttk.Checkbutton(self.threat_select_frame, variable=self.include_sre)
        self.th_ch_inc_sre.grid(row=2, column=3, padx=10, pady=3, sticky='ew')
        self.th_l_inc_scs = ttk.Label(self.threat_select_frame, text="Include SpaceCargoShips")
        self.th_l_inc_scs.grid(row=3, column=2, padx=10, pady=3, sticky='ew')
        self.th_ch_inc_scs = ttk.Checkbutton(self.threat_select_frame, variable=self.include_scs)
        self.th_ch_inc_scs.grid(row=3, column=3, padx=10, pady=3, sticky='ew')

        self.threat_output_frame = ttk.Frame(self.threat_tab)
        self.threat_output_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.threat_output_frame.grid_columnconfigure(0, weight=1)
        self.threat_output_frame.grid_rowconfigure(0, weight=1)

        self.threat_sg_tree = ttk.Treeview(self.threat_output_frame)
        self.threat_sg_tree["columns"] = ["Triggered", "Faction", "SpaceRandomEncounter", "SpaceCargoShip"]
        self.threat_sg_tree.column("#0", width=350, stretch=False)
        self.threat_sg_tree.heading("#0", text="SpawnGroup")
        for a_col in self.threat_sg_tree["columns"]:
            self.threat_sg_tree.column(a_col, width=50)
            self.threat_sg_tree.heading(a_col, text=a_col)
        self.threat_sg_tree.insert("", 1, "", text="No data loaded...", values=(""))

        self.threat_sg_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.threat_sg_tree_yscroll = ttk.Scrollbar(
            self.threat_output_frame, orient='vertical', command=self.threat_sg_tree.yview)
        self.threat_sg_tree.configure(yscrollcommand=self.threat_sg_tree_yscroll.set)

        self.threat_sg_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

        self.f_main.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.tabs.grid(row=0, column=2, rowspan=99, padx=5, pady=5, sticky='nsew')

        self.f_main.grid_columnconfigure(2, weight=1)
        self.f_main.grid_rowconfigure(98, weight=1)

    def import_from_sbc(self):
        self.parent_file_path = filedialog.askdirectory()
        print("Successfully imported a file path!")
        print(self.parent_file_path)
        returned_spawngroup_data = import_spawngroups(self.parent_file_path)
        self.spawngroup_dict = returned_spawngroup_data['data']
        self.populate_spawngroups()
        returned_component_data = import_components(self.parent_file_path)
        self.component_dict = returned_component_data['data']
        self.populate_components()

        self.populate_summary(returned_spawngroup_data['summary'], returned_component_data['summary'])
        self.populate_details(returned_component_data['detail'])

        self.b_lm_exp_csv["state"] = "normal"
        self.b_lm_exp_json["state"] = "normal"

    def populate_summary(self, sg_summ_dict, comp_summ_dict):
        self.summ_frame = ttk.Frame(self.summ_tab)
        self.summ_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        ttk.Label(
            self.summ_frame, text="MES SpawnGroup Summary", style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, padx=10, sticky='ew')
        row_counter = 1
        for key, value in sg_summ_dict.items():
            ttk.Label(
                self.summ_frame, text=f'{key}: '
            ).grid(row=row_counter, column=0, padx=10, sticky='e')
            ttk.Label(
                self.summ_frame, text=value, font=('Arial', 12, 'bold'), foreground="#7290f6"
            ).grid(row=row_counter, column=1, padx=10, sticky='w')
            row_counter += 1

        ttk.Label(
            self.summ_frame, text="RivalAI Component Summary", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
        row_counter += 1
        for key, value in comp_summ_dict.items():
            ttk.Label(
                self.summ_frame, text=f'{key}: '
            ).grid(row=row_counter, column=0, padx=10, sticky='e')
            ttk.Label(
                self.summ_frame, text=value, font=('Arial', 12, 'bold'), foreground="#7290f6"
            ).grid(row=row_counter, column=1, padx=10, sticky='w')
            row_counter += 1

    def populate_details(self, comp_det_dict):
        self.det_frame.grid_forget()

        self.det_frame = ttk.Frame(self.det_tab)
        self.det_frame.grid_columnconfigure(1, weight=1)

        row_counter = 2

        ttk.Label(
            self.det_frame, text="RivalAI Component Details", style="Header.TLabel", foreground="#7290f6"
        ).grid(row=0, column=0, columnspan=2, padx=10, sticky='ew')

        ttk.Label(
            self.det_frame, text="Unused Components:", style="Header.TLabel"
        ).grid(row=1, column=0, columnspan=2, padx=10, sticky='ew')

        if comp_det_dict['unused_comps']:
            for value in comp_det_dict['unused_comps']:
                print(value)
                ttk.Label(
                    self.det_frame, text=value[0], anchor=tk.W
                ).grid(row=row_counter, column=0, padx=10, sticky='ew')
                ttk.Label(
                    self.det_frame, text=value[1], anchor=tk.W
                ).grid(row=row_counter, column=1, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="Referenced Components that do not exist:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['noexist_comps']:
            for value in comp_det_dict['noexist_comps']:
                ttk.Label(
                    self.det_frame, text=value, anchor=tk.W
                ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="Duplicated Components:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['duplicate_data']:
            for key, value in comp_det_dict['duplicate_data'].items():
                ttk.Label(
                    self.det_frame, text=f'"{key}" shows up in: ', anchor=tk.W
                ).grid(row=row_counter, column=0, padx=10, sticky='ew')
                ttk.Label(
                    self.det_frame, text=',\n'.join(value), anchor=tk.W
                ).grid(row=row_counter, column=1, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="File Errors:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['file_errors']:
            for value in comp_det_dict['file_errors']:
                ttk.Label(
                    self.det_frame, text=value, anchor=tk.w
                ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=0, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        self.det_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def populate_spawngroups(self):
        self.sg_tree = ttk.Treeview(self.sg_tab)
        self.sg_tree["columns"] = ["Triggered", "Faction", "SpaceRandomEncounter", "SpaceCargoShip"]
        self.sg_tree.column("#0", width=350, stretch=False)
        self.sg_tree.heading("#0", text="SpawnGroup", anchor=tk.W)
        for a_col in self.sg_tree["columns"]:
            self.sg_tree.column(a_col, width=50)
            self.sg_tree.heading(a_col, text=a_col, anchor=tk.W)

        ordered_sgs = []
        for key in self.spawngroup_dict:
            ordered_sgs.append(key)
        ordered_sgs.sort()

        for key in ordered_sgs:
            if self.debug:
                print(f'adding key {key}')
            td = self.spawngroup_dict[key]
            last_iid = self.sg_tree.insert(
                "",
                9999,
                "",
                text=key,
                values=(td["TriggeredOnly"], td["FactionOwner"], td["SpaceCargoShip"], td["SpaceRandomEncounter"])
            )
            for a_key, a_value in td.items():
                if a_key == "Prefabs":
                    prefab_iid = self.sg_tree.insert(last_iid, 9999, "", text=a_key)
                    for a_dict in a_value:
                        self.sg_tree.insert(prefab_iid, 9999, "",
                                            text=a_dict["Prefab"],
                                            values=(f'{a_dict["Behaviour"]}', ))
                else:
                    self.sg_tree.insert(last_iid, 1, "", text=a_key, values=(f"{a_value}", ))

        self.sg_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.sg_tree_yscroll = ttk.Scrollbar(
            self.sg_tab, orient='vertical', command=self.sg_tree.yview)
        self.sg_tree.configure(yscrollcommand=self.sg_tree_yscroll.set)
        self.sg_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

    def populate_components(self):
        self.comp_tree = ttk.Treeview(self.comp_tab)
        self.comp_tree.configure(style='TNotebook')
        self.comp_tree["columns"] = "type"
        self.comp_tree.column("#0", width=500, stretch=False)
        self.comp_tree.column("type", width=100)
        self.comp_tree.heading("#0", text="SubTypeId", anchor=tk.W)
        self.comp_tree.heading("type", text="Type", anchor=tk.W)

        unordered_comps = {}
        for key in self.component_dict:
            if self.component_dict[key]["type"] == 'Behavior':
                unordered_comps[self.component_dict[key]["name"]] = key

        all_behaviors = [a_key for a_key in unordered_comps.keys()]
        all_behaviors.sort()

        index_increment = 0
        for a_behavior in all_behaviors:
            key = unordered_comps[a_behavior]
        # for key in self.component_dict:
        #     if self.component_dict[key]["type"] == 'Behavior':
        #     print(f'adding key {key}')
            index_increment += 1
            last_iid = self.comp_tree.insert(
                "",
                index_increment,
                "",
                text=self.component_dict[key]["name"],
                values=(self.component_dict[key]["type"])
            )
            for a_key in self.component_dict[key]['calls']:
                self.add_comp_node(a_key, last_iid)

        self.comp_tree.bind('<<TreeviewOpen>>', self.handle_open_event)
        self.comp_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.comp_tree_yscroll = ttk.Scrollbar(
            self.comp_tab, orient='vertical', command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=self.comp_tree_yscroll.set)
        self.comp_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

    def add_comp_node(self, this_key, last_iid):
        # for item_key, item_value in comp_dict[this_key].items():
        if self.debug:
            print(f'adding key {this_key}')
        last_iid = self.comp_tree.insert(
            last_iid,
            9999,
            "",
            text=self.component_dict[this_key]["name"],
            values=(self.component_dict[this_key]["type"])
        )
        for a_key in self.component_dict[this_key]['calls']:
            self.add_comp_node(a_key, last_iid)

    def handle_open_event(self, event):
        self.open_children(self.comp_tree.focus())

    def open_children(self, parent):
        self.comp_tree.item(parent, open=True)
        for child in self.comp_tree.get_children(parent):
            self.open_children(child)

    def get_threat_sgs(self):
        include_sre = True
        if self.include_sre.get() == 0:
            include_sre = False

        include_scs = True
        if self.include_scs.get() == 0:
            include_scs = False

        include_non_triggeredonly = True
        if self.include_non_triggeredonly.get() == 0:
            include_non_triggeredonly = False

        include_triggeredonly = True
        if self.include_triggeredonly.get() == 0:
            include_triggeredonly = False

        self.threat_sg_tree = ttk.Treeview(self.threat_output_frame)
        self.threat_sg_tree["columns"] = ["Triggered", "Min Threat", "Max Threat", "Faction", "SpaceRandomEncounter", "SpaceCargoShip"]
        self.threat_sg_tree.column("#0", width=350, stretch=False)
        self.threat_sg_tree.heading("#0", text="SpawnGroup", anchor=tk.W)
        for a_col in self.threat_sg_tree["columns"]:
            self.threat_sg_tree.column(a_col, width=50)
            self.threat_sg_tree.heading(a_col, text=a_col, anchor=tk.W)

        ordered_sgs = []
        for key in self.spawngroup_dict:
            ordered_sgs.append(key)
        ordered_sgs.sort()

        for key in ordered_sgs:
            if self.debug:
                print(f'Evaluating key {key}')
            td = self.spawngroup_dict[key]
            include_this = False
            if include_triggeredonly and td['TriggeredOnly'] == "true":
                include_this = True
            if include_non_triggeredonly and td['TriggeredOnly'] == "false":
                include_this = True
            if include_sre and td['SpaceRandomEncounter'] == "true":
                include_this = True
            if include_scs and td['SpaceCargoShip'] == "true":
                include_this = True

            if include_this:
                player_threat = self.player_threat_value.get()
                tsmin = int(td['ThreatScoreMinimum'])
                tsmax = int(td['ThreatScoreMaximum'])
                if player_threat != -1:
                    if tsmin != -1 and tsmin > player_threat:
                        include_this = False
                    if tsmax != -1 and tsmax < player_threat:
                        include_this = False

            if include_this:
                last_iid = self.threat_sg_tree.insert(
                    "",
                    9999,
                    "",
                    text=key,
                    values=(td["TriggeredOnly"], td['ThreatScoreMinimum'], td['ThreatScoreMaximum'],
                            td["FactionOwner"], td["SpaceCargoShip"], td["SpaceRandomEncounter"])
                )
                for a_key, a_value in td.items():
                    if a_key == "Prefabs":
                        prefab_iid = self.threat_sg_tree.insert(last_iid, 9999, "", text=a_key)
                        for a_dict in a_value:
                            self.threat_sg_tree.insert(prefab_iid, 9999, "",
                                                text=a_dict["Prefab"],
                                                values=(f'{a_dict["Behaviour"]}', ))
                    else:
                        self.threat_sg_tree.insert(last_iid, 1, "", text=a_key, values=(f"{a_value}", ))

        self.threat_sg_tree_yscroll = ttk.Scrollbar(
            self.threat_output_frame, orient='vertical', command=self.threat_sg_tree.yview)
        self.threat_sg_tree.configure(yscrollcommand=self.threat_sg_tree_yscroll.set)

        self.threat_sg_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.threat_sg_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

    def export_to_csv(self):
        # =======================================================================================
        # Write the results out to a simple csv report, format as we go
        # =======================================================================================

        print('Creating Spawngroup report file...')

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

        if self.debug:
            print('Imported Keys:')
            for this_key in keys_to_report_on:
                print(f'    {this_key}')
            print('\n')

        with open('export_spawngroups.csv', 'w', newline='') as csv_file:
            headers = [
                'TriggeredOnly',
                'SubtypeId',
                'IsPirate',
                'Frequency',
                'Prefabs'
            ]
            all_fields = headers + keys_to_report_on

            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow(all_fields)

            print('Generating report...')

            for each_sg in self.spawngroup_dict:
                if len(each_sg) == 0:
                    continue
                triggered_only = 'false'
                if (self.spawngroup_dict[each_sg]['SpaceCargoShip'] == 'false' and
                        self.spawngroup_dict[each_sg]['SpaceRandomEncounter'] == 'false' and
                        self.spawngroup_dict[each_sg]['LunarCargoShip'] == 'false' and
                        self.spawngroup_dict[each_sg]['AtmosphericCargoShip'] == 'false' and
                        self.spawngroup_dict[each_sg]['PlanetaryInstallation'] == 'false'):
                    self.spawngroup_dict[each_sg]['TriggeredOnly'] = 'true'
                else:
                    self.spawngroup_dict[each_sg]['TriggeredOnly'] = 'false'

                this_row = [triggered_only]
                for a_field in all_fields:
                    if a_field == 'Prefabs':
                        prefab_str = ''
                        for each_prefab in self.spawngroup_dict[each_sg]['Prefabs']:
                            # tp = all_sg[each_sg]['Prefabs'][each_prefab]
                            if len(prefab_str) > 0:
                                prefab_str = prefab_str + '\n'
                            prefab_str = f"{prefab_str}{each_prefab['Prefab']} - {each_prefab['Behaviour']} " \
                                f"({each_prefab['X']}, {each_prefab['Y']}, {each_prefab['Z']}) " \
                                f"{each_prefab['Speed']}m/s"
                        this_row.append(f'{prefab_str}')
                    elif a_field == 'TriggeredOnly':
                        continue
                    else:
                        this_row.append(f'{self.spawngroup_dict[each_sg][a_field]}')
                csv_writer.writerow(this_row)

        print('Spawngroup Report generated and written successfully!')

        print('Creating components report file...')

        with open('export_components.csv', 'w', newline='') as csv_file:
            headers = [
                'Key',
                'Name',
                'Type',
                'Description',
                'File',
                'Child Components'
            ]

            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow(headers)

            print('Generating report...')

            for comp_key in self.component_dict:
                this_comp = self.component_dict[comp_key]

                this_row = [
                    comp_key,
                    this_comp['name'],
                    this_comp['type'],
                    this_comp['desc'],
                    this_comp['file'],
                    ', '.join([str(a_call) for a_call in this_comp['calls']])
                ]
                csv_writer.writerow(this_row)

        print('Component report generated and written successfully!')

    def export_to_json(self):
        with open('export_spawngroups.json', 'w') as json_file:
            json_file.write(json.dumps(self.spawngroup_dict, indent=2))

        with open("export_components.json", 'w') as json_file:
            json.dump(self.component_dict, json_file, indent=2)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("900x600")

    raim = RAIMapper(root)

    root.mainloop()
