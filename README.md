# RAI-Mapper
A tool for managing mods built using Lucas/Meridius IX's "Modular Encounter Spawner"

This is a GUI based tool that can load an MES mod into a custom dataset that allows you to quickly get an overview, analyze spawngroups and RAI components, and get a detailed report of potential issues. 

## **How to use**

Click the blue "Load" button in the top left. This will open a dialog box where you can select the parent directory (or any sub-directory if you prefer) of your MES mod. The program then goes through the entire directory tree looking for .sbc files. For every .sbc file it finds, it walks the XML structure looking for MES and RAI spawngroups, components, and prefabs, then loads them into memory. You can then dig into the compiled data using the tabs at the top.

## **Tabs**

__Summary__: This gives you a summary of what was scanned and found by RAI-Mapper

__Details__: This tab shows you potential issues that the program detected.
* __Unused Components__: These are components that were not called by any behaviors. They may be indicative of an error, or they may be components that are only used conditionally (like an autopilot profile that is switched to by a trigger and action).
* __Referenced Components that do not exist__: When a component calls a child component (A trigger with `[Actions:my_action]`, for example), but the referenced component cannot be found, the name of the missing component is reported here.
* __Duplicated Components__: When a component is found more than once, it is reported here. RAI will overwrite a component each time a new component with the same name is found, and this could indicate copy/paste errors.
* __File Erros__: When a file cannot be properly parsed (missing closing tag, etc.), it will show up here. Please note that this catches XML file errors and *not* SBC file errors specifically. Space Engineers SBCs use more stringent rules when determining if an SBC is valid.

__Spawn Groups__: This tab shows you all of the discovered spawngroups that RAI-Mapper found. It is a tree structure and you can expand any spawngroup to see additional details, including the prefabs the spawngroup uses and their associated behaviors.

__RAI Components__: This tab shows you all of the discovered RAI Components that RAI-Mapper found. It is a tree structure and you can expand any Behavior to see the child components (triggers, triggergroups, etc.), and their children, and their children, and...

__SG Filter__: This tab is much like the __Spawn Groups__ tab, except that it allows you to filter the list of all spawn groups to show only the subset that matches your filters. Useful for seeing all spawns at a particular player threat score, or just to see all SpaceCargoShips, etc. Use the checkboxes to select the things you want to appear, for something to be filtered out, it must not match *any* criteria. To not filter by threat score, use a value of -1 (the default).
* __Include Spawned Encounters__ This option includes any encoutner which can be spawned by MES types (SpaceCargoShip, SpaceRandomEncounter, etc.). This will override the behavior of the specific encounter types and include them all (regardless of their settings), if you want to filter explicitly by type, make sure this box is not checked.
* __Include Triggered-Only Encounters__ This option includes any encoutner which *cannot* be spawned by MES, but can be spawned by RAI Spawn components.
* __Everything Else__: These should be pretty obvious?

## **Exporting Data**

__Export CSV__: This button will enable once data is loaded and allows you to create two .csv files (*export_spawngroups.csv* and *export_components.csv*) that contain all of the data discovered by RAI-Mapper. This is useful for advanced sorting and analysis tasks that RAI-Mapper doesn't do matively.

__Export CSV__: This button will enable once data is loaded and allows you to create two .json files (*export_spawngroups.json* and *export_components.json*) that is a json representation of the RAI-Mapper internal dataset. These are human readable and should allow you to quicly get information that you can't access natively in RAI-Mapper.


Please enjoy, and happy modding!
-Old Man Katan
