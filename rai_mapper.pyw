import re
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
        self.root = root
        self.root.title("RAI-Mapper")
        self.chk_thr = self.root.register(check_threat)

        icon_photo = tk.PhotoImage(file=r"inc\se_icon.png")
        self.root.wm_iconphoto(False, icon_photo)

        self.parent_file_path = ''
        self.spawngroup_dict = {}
        self.component_dict = {}

        self.sg_player_threat_value = tk.IntVar()
        self.sg_player_threat_value.set(-1)
        self.sg_threat_faction_filter = tk.StringVar()
        self.sg_threat_faction_filter.set("")
        self.sg_match_name_filter = tk.StringVar()
        self.sg_match_name_filter.set("")
        self.sg_not_name_filter = tk.StringVar()
        self.sg_not_name_filter.set("")
        self.sg_include_non_triggeredonly = tk.IntVar()
        self.sg_include_non_triggeredonly.set(0)
        self.sg_include_triggeredonly = tk.IntVar()
        self.sg_include_triggeredonly.set(1)

        self.sg_include_acs = tk.IntVar()
        self.sg_include_acs.set(1)
        self.sg_include_lcs = tk.IntVar()
        self.sg_include_lcs.set(1)
        self.sg_include_pi = tk.IntVar()
        self.sg_include_pi.set(1)
        self.sg_include_sre = tk.IntVar()
        self.sg_include_sre.set(1)
        self.sg_include_scs = tk.IntVar()
        self.sg_include_scs.set(1)

        self.sg_include_territory = tk.IntVar()
        self.sg_include_territory.set(0)

        self.ec_match_in_name = tk.StringVar()
        self.ec_match_in_name.set("")
        self.ec_include_mes_comp = tk.IntVar()
        self.ec_include_mes_comp.set(0)
        self.ec_include_rai_comp = tk.IntVar()
        self.ec_include_rai_comp.set(1)
        self.ec_include_behavior = tk.IntVar()
        self.ec_include_behavior.set(1)
        self.ec_include_dereliction = tk.IntVar()
        self.ec_include_dereliction.set(0)

        self.debug = False

        self.style = ttk.Style()
        # print(self.style.theme_names())

        self.style.theme_create(
            "raim_theme", parent="", settings={
                ".": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#C3C3C3",
                        "relief": "flat",
                        "font": ('Arial', 12),
                        "borderwidth": 0
                    }
                },
                "TCheckbutton": {
                    "configure": {
                        "background": "#303030",
                        "compound": "#C3C3C3",
                        "foreground": "#4260d6",
                        "indicatorbackground": "#303030",
                        "indicatorcolor": "#C3C3C3",
                        "relief": "flat",
                        "indicatorrelief": "flat",
                        "indicatordiameter": 20,
                        "indicatormargin": 0,
                        "borderwidth": 2
                    },
                    "map": {
                        "indicatorcolor": [("selected", "#4260d6")],
                        "indicatorrelief": [("selected", "groove")],
                        "bordercolor": [("selected", "#4260d6")],
                    }

                },
                "TEntry": {
                    "configure": {
                        "background": "#303030",
                        "foreground": "#4260d6",
                        "padding": 2,
                        "margin": 0
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
                        # "relief": "groove",
                        # "borderwidth": 2,
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
                        "troughcolor": "#505050"
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
        self.l_lm_title.grid(row=0, column=0, padx=10, pady=20, sticky='ew')

        self.sep_lm_sep10 = ttk.Separator(self.f_main)
        self.sep_lm_sep10.grid(row=10, column=0, padx=20, pady=7, sticky='ew')

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
        self.b_lm_load.grid(row=11, column=0, padx=10, pady=2, sticky='ew')

        self.sep_lm_sep20 = ttk.Separator(self.f_main)
        self.sep_lm_sep20.grid(row=20, column=0, padx=20, pady=7, sticky='ew')

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
        self.b_lm_exp_csv.grid(row=21, column=0, padx=10, pady=2, sticky='ew')

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
        self.b_lm_exp_json.grid(row=22, column=0, padx=10, pady=2, sticky='ew')

        self.sep_lm_sep50 = ttk.Separator(self.f_main)
        self.sep_lm_sep50.grid(row=50, column=0, padx=20, pady=7, sticky='ew')

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
        self.b_lm_quit.grid(row=98, column=0, padx=10, pady=10, sticky='ew')

        self.sep_lm_sepright = ttk.Separator(self.f_main, orient=tk.VERTICAL)
        self.sep_lm_sepright.grid(row=0, column=1, rowspan=99, padx=5, pady=5, sticky='ns')

        self.tabs = ttk.Notebook(self.f_main)

        # #############################################
        # SUMMARY
        # #############################################

        self.summ_tab = ttk.Frame(self.tabs)
        self.summ_tab.grid_columnconfigure(0, weight=1)
        self.summ_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.summ_tab, text='Summary')

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

        # #############################################
        # DETAILS
        # #############################################

        self.det_tab = ttk.Frame(self.tabs)
        self.det_tab.grid_columnconfigure(0, weight=1)
        self.det_tab.grid_rowconfigure(0, weight=1)

        self.tabs.add(self.det_tab, text='Details')

        self.det_canvas = tk.Canvas(self.det_tab, bg='#303030', borderwidth=0, relief='flat', highlightthickness=0)
        self.det_canvas.grid_columnconfigure(0, weight=1)
        self.det_canvas.grid_rowconfigure(0, weight=1)

        self.det_frame_yscroll = ttk.Scrollbar(
            self.det_tab, orient='vertical', command=self.det_canvas.yview)

        self.det_frame = ttk.Frame(self.det_canvas)

        self.det_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.det_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.canvas_item = self.det_canvas.create_window(0, 0, anchor='nw', window=self.det_frame)
        self.det_canvas.update_idletasks()

        self.det_canvas.config(scrollregion=self.det_canvas.bbox("all"),
                               yscrollcommand=self.det_frame_yscroll.set)
        self.det_canvas.grid(row=0, column=0, sticky='nsew')
        self.det_frame_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

        self.det_frame.grid_columnconfigure(0, minsize=50)
        self.det_frame.grid_columnconfigure(2, weight=1)
        self.det_frame.grid_rowconfigure(98, weight=1)

        # self.det_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.l_det_nodata = ttk.Label(
            self.det_frame,
            text='No data loaded.\n',
            style='Header.TLabel'
        )
        self.l_det_nodata.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        self.det_frame.bind("<Configure>", self.OnFrameConfigure)
        self.det_canvas.bind('<Configure>', self.FrameWidth)

        # #############################################
        # SPAWNGROUPS
        # #############################################

        self.sg_tab = ttk.Frame(self.tabs)
        self.sg_tab.grid_columnconfigure(0, weight=1)
        self.sg_tab.grid_rowconfigure(1, weight=1)

        self.tabs.add(self.sg_tab, text='SpawnGroups')

        self.sg_select_frame = ttk.Frame(self.sg_tab)
        self.sg_select_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.sg_select_frame.grid_columnconfigure(98, weight=1)
        self.sg_select_frame.grid_rowconfigure(98, weight=1)

        self.sg_e_player_threat = ttk.Entry(
            self.sg_select_frame,
            font=("Calibri", 12),
            textvariable=self.sg_player_threat_value,
            validate='key',
            validatecommand=(self.chk_thr, '%P'),
            width=10
        )
        self.sg_e_player_threat.grid(row=0, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.sg_l_player_threat = ttk.Label(self.sg_select_frame, text="Player Threat")
        self.sg_l_player_threat.grid(row=0, column=2, padx=3, pady=3, sticky='w')

        self.sg_e_faction_filter = ttk.Entry(
            self.sg_select_frame,
            font=("Calibri", 12),
            textvariable=self.sg_threat_faction_filter,
            validate='key',
            width=10
        )
        self.sg_e_faction_filter.grid(row=1, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.sg_l_faction_filter = ttk.Label(self.sg_select_frame, text="Match in Faction")
        self.sg_l_faction_filter.grid(row=1, column=2, padx=3, pady=3, sticky='w')

        self.sg_e_match_name_filter = ttk.Entry(
            self.sg_select_frame,
            font=("Calibri", 12),
            textvariable=self.sg_match_name_filter,
            validate='key',
            width=10
        )
        self.sg_e_match_name_filter.grid(row=2, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.sg_l_match_name_filter = ttk.Label(self.sg_select_frame, text="Match in Name")
        self.sg_l_match_name_filter.grid(row=2, column=2, padx=3, pady=3, sticky='w')

        self.sg_e_not_name_filter = ttk.Entry(
            self.sg_select_frame,
            font=("Calibri", 12),
            textvariable=self.sg_not_name_filter,
            validate='key',
            width=10
        )
        self.sg_e_not_name_filter.grid(row=3, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.sg_l_not_name_filter = ttk.Label(self.sg_select_frame, text="Filter in Name")
        self.sg_l_not_name_filter.grid(row=3, column=2, padx=3, pady=3, sticky='w')

        self.sg_ch_inc_scs = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_acs)
        self.sg_ch_inc_scs.grid(row=0, column=3, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_scs = ttk.Label(self.sg_select_frame, text="Include AtmosphericCargoShips")
        self.sg_l_inc_scs.grid(row=0, column=4, padx=10, pady=3, sticky='ew')

        self.sg_ch_inc_scs = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_lcs)
        self.sg_ch_inc_scs.grid(row=1, column=3, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_scs = ttk.Label(self.sg_select_frame, text="Include LunarCargoShips")
        self.sg_l_inc_scs.grid(row=1, column=4, padx=10, pady=3, sticky='ew')

        self.sg_ch_inc_scs = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_pi)
        self.sg_ch_inc_scs.grid(row=2, column=3, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_scs = ttk.Label(self.sg_select_frame, text="Include PlanetaryInstallation")
        self.sg_l_inc_scs.grid(row=2, column=4, padx=10, pady=3, sticky='ew')

        self.sg_ch_inc_scs = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_scs)
        self.sg_ch_inc_scs.grid(row=3, column=3, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_scs = ttk.Label(self.sg_select_frame, text="Include SpaceCargoShips")
        self.sg_l_inc_scs.grid(row=3, column=4, padx=10, pady=3, sticky='ew')

        self.sg_ch_inc_sre = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_sre)
        self.sg_ch_inc_sre.grid(row=4, column=3, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_sre = ttk.Label(self.sg_select_frame, text="Include SpaceRandomEncounters")
        self.sg_l_inc_sre.grid(row=4, column=4, padx=10, pady=3, sticky='ew')

        self.sg_b_get_sg = tk.Button(
            self.sg_select_frame,
            text="Filter SpawnGroups",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.populate_sgs,
            anchor=tk.CENTER
        )
        self.sg_b_get_sg.grid(row=10, column=0, padx=10, pady=[10, 3], sticky='ew', columnspan=3)

        self.sg_b_get_sg = tk.Button(
            self.sg_select_frame,
            text="Clear Filters",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.clear_sg_filter,
            anchor=tk.CENTER
        )
        self.sg_b_get_sg.grid(row=10, column=3, padx=10, pady=[10, 3], sticky='ew', columnspan=2)

        self.sg_ch_inc_notrig = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_non_triggeredonly)
        self.sg_ch_inc_notrig.grid(row=0, column=5, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_notrig = ttk.Label(self.sg_select_frame, text="Include Spawned Encounters")
        self.sg_l_inc_notrig.grid(row=0, column=6, padx=10, pady=3, sticky='ew')

        self.sg_ch_inc_trig = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_triggeredonly)
        self.sg_ch_inc_trig.grid(row=1, column=5, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_trig = ttk.Label(self.sg_select_frame, text="Include Triggered-Only Encounters")
        self.sg_l_inc_trig.grid(row=1, column=6, padx=10, pady=3, sticky='ew')

        self.sg_sep_c3_1 = ttk.Separator(self.sg_select_frame)
        self.sg_sep_c3_1.grid(row=2, column=5, columnspan=2, padx=20, pady=7, sticky='ew')

        self.sg_ch_inc_territory = ttk.Checkbutton(self.sg_select_frame, variable=self.sg_include_territory)
        self.sg_ch_inc_territory.grid(row=3, column=5, padx=10, pady=3, sticky='ew')
        self.sg_l_inc_territory = ttk.Label(self.sg_select_frame, text="Include Territories")
        self.sg_l_inc_territory.grid(row=3, column=6, columnspan=2, padx=10, pady=3, sticky='ew')

        self.sg_sep_bottom = ttk.Separator(self.sg_select_frame)
        self.sg_sep_bottom.grid(row=99, column=0, columnspan=98, padx=20, pady=7, sticky='ew')

        self.sg_output_frame = ttk.Frame(self.sg_tab)
        self.sg_output_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.sg_output_frame.grid_columnconfigure(0, weight=1)
        self.sg_output_frame.grid_rowconfigure(0, weight=1)

        self.sg_tree = ttk.Treeview(self.sg_output_frame)

        self.populate_sgs()
        self.sg_tree_yscroll = ttk.Scrollbar(
            self.sg_output_frame, orient='vertical', command=self.sg_tree.yview)

        # #############################################
        # ENTITYCOMPONENTS
        # #############################################

        self.comp_tab = ttk.Frame(self.tabs)
        self.comp_tab.grid_columnconfigure(0, weight=1)
        self.comp_tab.grid_rowconfigure(1, weight=1)

        self.tabs.add(self.comp_tab, text='EntityComponents')

        self.ec_select_frame = ttk.Frame(self.comp_tab)
        self.ec_select_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.ec_select_frame.grid_columnconfigure(98, weight=1)
        self.ec_select_frame.grid_rowconfigure(98, weight=1)

        self.ec_e_comp_name = ttk.Entry(
            self.ec_select_frame,
            font=("Calibri", 12),
            textvariable=self.ec_match_in_name,
            validate='key',
            width=10
        )
        self.ec_e_comp_name.grid(row=0, column=0, columnspan=2, padx=10, pady=3, sticky='w')
        self.ec_l_comp_name = ttk.Label(self.ec_select_frame, text="Match in Name")
        self.ec_l_comp_name.grid(row=0, column=2, padx=3, pady=3, sticky='w')

        self.ec_ch_inc_scs = ttk.Checkbutton(self.ec_select_frame, variable=self.ec_include_rai_comp)
        self.ec_ch_inc_scs.grid(row=0, column=3, padx=10, pady=3, sticky='ew')
        self.ec_l_inc_scs = ttk.Label(self.ec_select_frame, text="Include RAI Components")
        self.ec_l_inc_scs.grid(row=0, column=4, padx=10, pady=3, sticky='ew')

        self.ec_ch_inc_scs = ttk.Checkbutton(self.ec_select_frame, variable=self.ec_include_mes_comp)
        self.ec_ch_inc_scs.grid(row=1, column=3, padx=10, pady=3, sticky='ew')
        self.ec_l_inc_scs = ttk.Label(self.ec_select_frame, text="Include MES Components")
        self.ec_l_inc_scs.grid(row=1, column=4, padx=10, pady=3, sticky='ew')

        self.ec_b_get_sg = tk.Button(
            self.ec_select_frame,
            text="Filter EntityComponents",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.populate_ecs,
            anchor=tk.CENTER
        )
        self.ec_b_get_sg.grid(row=10, column=0, padx=10, pady=[10, 3], sticky='ew', columnspan=3)

        self.ec_b_get_sg = tk.Button(
            self.ec_select_frame,
            text="Clear Filters",
            relief="flat",
            background="#4260d6",
            foreground="#C3C3C3",
            font=('Arial', 16, 'bold'),
            padx=10,
            command=self.clear_ec_filter,
            anchor=tk.CENTER
        )
        self.ec_b_get_sg.grid(row=10, column=3, padx=10, pady=[10, 3], sticky='ew', columnspan=2)

        self.ec_ch_inc_behav = ttk.Checkbutton(self.ec_select_frame, variable=self.ec_include_behavior)
        self.ec_ch_inc_behav.grid(row=0, column=5, padx=10, pady=3, sticky='ew')
        self.ec_l_inc_behav = ttk.Label(self.ec_select_frame, text="Include Behavior")
        self.ec_l_inc_behav.grid(row=0, column=6, padx=10, pady=3, sticky='ew')

        self.ec_ch_inc_derel = ttk.Checkbutton(self.ec_select_frame, variable=self.ec_include_dereliction)
        self.ec_ch_inc_derel.grid(row=1, column=5, padx=10, pady=3, sticky='ew')
        self.ec_l_inc_derel = ttk.Label(self.ec_select_frame, text="Include Dereliction")
        self.ec_l_inc_derel.grid(row=1, column=6, padx=10, pady=3, sticky='ew')

        self.ec_sep_bottom = ttk.Separator(self.ec_select_frame)
        self.ec_sep_bottom.grid(row=99, column=0, columnspan=98, padx=20, pady=7, sticky='ew')

        self.ec_output_frame = ttk.Frame(self.comp_tab)
        self.ec_output_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.ec_output_frame.grid_columnconfigure(0, weight=1)
        self.ec_output_frame.grid_rowconfigure(0, weight=1)

        self.comp_tree = ttk.Treeview(self.ec_output_frame)
        self.comp_tree_yscroll = ttk.Scrollbar(
            self.ec_output_frame, orient='vertical', command=self.comp_tree.yview)
        self.populate_ecs()

        # #############################################
        # FRAME MAIN
        # #############################################

        self.f_main.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.tabs.grid(row=0, column=2, rowspan=99, padx=5, pady=5, sticky='nsew')

        self.f_main.grid_columnconfigure(2, weight=1)
        self.f_main.grid_rowconfigure(97, weight=1)

    def import_from_sbc(self):
        self.parent_file_path = filedialog.askdirectory()
        print("Successfully imported a file path!")
        print(self.parent_file_path)
        returned_spawngroup_data = import_spawngroups(self.parent_file_path)
        self.spawngroup_dict = returned_spawngroup_data['data']
        self.populate_sgs()

        returned_component_data = import_components(self.parent_file_path)
        self.component_dict = returned_component_data['data']
        self.populate_ecs()

        returned_component_data['detail']['noexist_sgs'] = []
        match_spawned_spawngroups = re.compile(r'\[SpawnGroups:(.*?)\]')
        for a_key in self.component_dict:
            if self.component_dict[a_key]["type"] == "Spawn":
                find_sp_sg = match_spawned_spawngroups.findall(self.component_dict[a_key]["desc"])
                for found_sg in find_sp_sg:
                    if found_sg not in self.spawngroup_dict:
                        returned_component_data['detail']['noexist_sgs'].append(
                            [found_sg, f'Called by: {self.component_dict[a_key]["name"]}']
                        )

        self.populate_summary(returned_spawngroup_data['summary'], returned_component_data['summary'])
        self.populate_details(returned_component_data['detail'])

        self.b_lm_exp_csv["state"] = "normal"
        self.b_lm_exp_json["state"] = "normal"

    def populate_summary(self, sg_summ_dict, comp_summ_dict):
        for widgets in self.summ_frame.winfo_children():
            widgets.destroy()

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
        row_counter = 2
        for widgets in self.det_frame.winfo_children():
            widgets.destroy()

        ttk.Label(
            self.det_frame, text="RivalAI Component Details", style="Header.TLabel", foreground="#7290f6"
        ).grid(row=0, column=0, columnspan=3, padx=10, sticky='ew')

        ttk.Label(
            self.det_frame, text="Unused Components:", style="Header.TLabel"
        ).grid(row=1, column=0, columnspan=3, padx=10, sticky='ew')

        if comp_det_dict['unused_comps']:
            for value in comp_det_dict['unused_comps']:
                print(value)
                ttk.Label(
                    self.det_frame, text=value[0], anchor=tk.W
                ).grid(row=row_counter, column=1, padx=10, sticky='ew')
                ttk.Label(
                    self.det_frame, text=value[1], anchor=tk.W
                ).grid(row=row_counter, column=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="Referenced Components that do not exist:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=3, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['noexist_comps']:
            for value in comp_det_dict['noexist_comps']:
                ttk.Label(
                    self.det_frame, text=value, anchor=tk.W
                ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="Spawngroups in Spawn Components that do not exist:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=3, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['noexist_sgs']:
            for value in comp_det_dict['noexist_sgs']:
                sg_name, spawn_comp_name = value
                ttk.Label(
                    self.det_frame, text=sg_name, anchor=tk.W
                ).grid(row=row_counter, column=1, columnspan=1, padx=10, sticky='ew')
                ttk.Label(
                    self.det_frame, text=spawn_comp_name, anchor=tk.W
                ).grid(row=row_counter, column=2, columnspan=1, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=0, columnspan=3, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="Duplicated Components:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=3, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['duplicate_data']:
            for key, value in comp_det_dict['duplicate_data'].items():
                ttk.Label(
                    self.det_frame, text=f'"{key}" shows up in: ', anchor=tk.W
                ).grid(row=row_counter, column=1, padx=10, sticky='ew')
                ttk.Label(
                    self.det_frame, text=',\n'.join(value), anchor=tk.W
                ).grid(row=row_counter, column=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        ttk.Label(
            self.det_frame, text="File Errors:", style="Header.TLabel"
        ).grid(row=row_counter, column=0, columnspan=3, padx=10, sticky='ew')
        row_counter += 1

        if comp_det_dict['file_errors']:
            for value in comp_det_dict['file_errors']:
                ttk.Label(
                    self.det_frame, text=value, anchor=tk.W
                ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
                row_counter += 1
        else:
            ttk.Label(
                self.det_frame, text="None", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        for i in range(0, 2):
            ttk.Label(
                self.det_frame, text=" ", anchor=tk.W
            ).grid(row=row_counter, column=1, columnspan=2, padx=10, sticky='ew')
            row_counter += 1

        self.det_canvas.update_idletasks()
        self.det_canvas.config(scrollregion=self.det_canvas.bbox("all"))

    def populate_sgs(self):
        match_faction = self.sg_threat_faction_filter.get()
        match_name = self.sg_match_name_filter.get()
        not_name = self.sg_not_name_filter.get()

        include_acs = True
        if self.sg_include_acs.get() == 0:
            include_acs = False

        include_lcs = True
        if self.sg_include_lcs.get() == 0:
            include_lcs = False

        include_pi = True
        if self.sg_include_pi.get() == 0:
            include_pi = False

        include_scs = True
        if self.sg_include_scs.get() == 0:
            include_scs = False

        include_sre = True
        if self.sg_include_sre.get() == 0:
            include_sre = False

        include_non_triggeredonly = True
        if self.sg_include_non_triggeredonly.get() == 0:
            include_non_triggeredonly = False

        include_triggeredonly = True
        if self.sg_include_triggeredonly.get() == 0:
            include_triggeredonly = False

        include_territory = True
        if self.sg_include_territory.get() == 0:
            include_territory = False

        for widgets in self.sg_output_frame.winfo_children():
            widgets.destroy()

        self.sg_tree = ttk.Treeview(self.sg_output_frame)
        self.sg_tree["columns"] = [
            "Triggered",
            "Min Threat",
            "Max Threat",
            "Faction",
            "SpaceRandomEncounter",
            "SpaceCargoShip"
        ]
        self.sg_tree.column("#0", width=350, stretch=False)
        self.sg_tree.heading("#0", text="SpawnGroup", anchor=tk.W)
        for a_col in self.sg_tree["columns"]:
            self.sg_tree.column(a_col, width=50)
            self.sg_tree.heading(a_col, text=a_col, anchor=tk.W)

        if len(self.spawngroup_dict) > 0:
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

                if include_acs and td['AtmosphericCargoShip'] == "true":
                    include_this = True
                if include_lcs and td['LunarCargoShip'] == "true":
                    include_this = True
                if include_pi and td['PlanetaryInstallation'] == "true":
                    include_this = True
                if include_scs and td['SpaceCargoShip'] == "true":
                    include_this = True
                if include_sre and td['SpaceRandomEncounter'] == "true":
                    include_this = True

                if include_this:
                    player_threat = self.sg_player_threat_value.get()
                    tsmin = int(td['ThreatScoreMinimum'])
                    tsmax = int(td['ThreatScoreMaximum'])
                    if player_threat != -1:
                        if tsmin != -1 and tsmin > player_threat:
                            include_this = False
                        if tsmax != -1 and tsmax < player_threat:
                            include_this = False

                if include_this and len(match_faction) > 0:
                    if td['FactionOwner'].find(match_faction) == -1:
                        include_this = False

                if include_this and len(match_name) > 0:
                    if key.find(match_name) == -1:
                        include_this = False

                if include_this and len(not_name) > 0:
                    if key.find(not_name) != -1:
                        include_this = False

                if include_this and not include_territory:
                    if td['IsTerritory'] == 'true':
                        include_this = False

                if include_this:
                    last_iid = self.sg_tree.insert(
                        "",
                        9999,
                        "",
                        text=key,
                        values=(td["TriggeredOnly"], td['ThreatScoreMinimum'], td['ThreatScoreMaximum'],
                                td["FactionOwner"], td["SpaceCargoShip"], td["SpaceRandomEncounter"])
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

        else:
            self.sg_tree.insert("", 1, "", text="No data loaded.", values=("", ))

        self.sg_tree_yscroll = ttk.Scrollbar(
            self.sg_output_frame, orient='vertical', command=self.sg_tree.yview)
        self.sg_tree.configure(yscrollcommand=self.sg_tree_yscroll.set)

        self.sg_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.sg_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

    def clear_sg_filter(self):
        self.sg_player_threat_value.set(-1)
        self.sg_threat_faction_filter.set("")
        self.sg_match_name_filter.set("")
        self.sg_not_name_filter.set("")
        self.sg_include_non_triggeredonly.set(0)
        self.sg_include_triggeredonly.set(1)

        self.sg_include_acs.set(1)
        self.sg_include_lcs.set(1)
        self.sg_include_pi.set(1)
        self.sg_include_sre.set(1)
        self.sg_include_scs.set(1)

        self.sg_include_territory.set(0)

        self.populate_sgs()

    def populate_ecs(self):
        for widgets in self.ec_output_frame.winfo_children():
            widgets.destroy()

        self.comp_tree = ttk.Treeview(self.ec_output_frame)
        self.comp_tree.configure(style='TNotebook')
        self.comp_tree["columns"] = "type"
        self.comp_tree.column("#0", width=500, stretch=False)
        self.comp_tree.column("type", width=100)
        self.comp_tree.heading("#0", text="SubTypeId", anchor=tk.W)
        self.comp_tree.heading("type", text="Type", anchor=tk.W)

        if len(self.component_dict) > 0:
            include_mes = False
            if self.ec_include_mes_comp.get() == 1:
                include_mes = True

            include_rai = False
            if self.ec_include_rai_comp.get() == 1:
                include_rai = True

            include_dereliction = False
            if self.ec_include_dereliction.get() == 1:
                include_dereliction = True

            include_behavior = False
            if self.ec_include_behavior.get() == 1:
                include_behavior = True

            unordered_comps = {}
            for key in self.component_dict:
                if self.component_dict[key]["type"] == 'Behavior':
                    unordered_comps[self.component_dict[key]["name"]] = key

            all_behaviors = [a_key for a_key in unordered_comps.keys()]
            all_behaviors.sort()

            index_increment = 0
            for a_behavior in all_behaviors:
                key = unordered_comps[a_behavior]
                td = self.component_dict[key]

                include_this = False

                if include_mes and td['comp_type'] == 'mes':
                    include_this = True

                if include_rai and td['comp_type'] == 'rai':
                    include_this = True

                if include_dereliction and td['type'] == 'Dereliction':
                    include_this = True

                if include_behavior and td['type'] == 'Behavior':
                    include_this = True

                match_in_name = self.ec_match_in_name.get()
                if len(match_in_name) > 0:
                    if td['name'].find(self.ec_match_in_name.get()) == -1:
                        include_this = False

                if include_this:
                    index_increment += 1
                    last_iid = self.comp_tree.insert(
                        "",
                        index_increment,
                        "",
                        text=td["name"],
                        values=(td["type"])
                    )
                    for a_key in td['calls']:
                        self.add_comp_node(a_key, last_iid)
        else:
            self.comp_tree.insert("", 1, "", text="No data loaded.", values=("", ))

        self.comp_tree.bind('<<TreeviewOpen>>', self.handle_open_event)
        self.comp_tree.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.comp_tree_yscroll = ttk.Scrollbar(
            self.ec_output_frame, orient='vertical', command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=self.comp_tree_yscroll.set)
        self.comp_tree_yscroll.grid(row=0, column=1, padx=5, pady=5, sticky='nse')

    def clear_ec_filter(self):
        self.ec_match_in_name.set("")
        self.ec_include_mes_comp.set(0)
        self.ec_include_rai_comp.set(1)
        self.ec_include_dereliction.set(0)
        self.ec_include_behavior.set(0)
        self.populate_ecs()

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
                this_row = [self.spawngroup_dict[each_sg]['TriggeredOnly']]
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

    def _bound_to_mousewheel(self, event):
        self.det_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.det_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.det_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def FrameWidth(self, event):
        canvas_width = event.width
        self.det_canvas.itemconfig(self.canvas_item, width=canvas_width)

    def OnFrameConfigure(self, event):
        self.det_canvas.configure(scrollregion=self.det_canvas.bbox("all"))


if __name__ == '__main__':
    tk_window = tk.Tk()
    tk_window.geometry("1200x600")

    raim = RAIMapper(tk_window)

    tk_window.mainloop()
