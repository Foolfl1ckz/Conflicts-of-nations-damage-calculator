# main.py
from data import unit_list, terrain_list, type_list
import dearpygui.dearpygui as dpg
import UnitClass as uc
import WindowClasses as wc




unit_name_map = {unit.name: unit for unit in unit_list}

# GUI setup
dpg.create_context()
dpg.create_viewport(title='ConDmgCalc', width=800, height=600)
dpg.setup_dearpygui()


def preload_windows():
    defending_window_tag = "defending_unit_window"
    defending_window = wc.DefendingUnitWindow(defending_window_tag, unit_name_map, terrain_list, type_list)
    dpg.hide_item(defending_window_tag) 
    saw_tag = "simple_attack_window"
    saw = wc.SimpleAttackWindow(saw_tag, unit_name_map, terrain_list, type_list)
    dpg.hide_item(saw_tag)  
    return defending_window_tag, saw_tag

defending_window_tag,saw_tag = preload_windows()

# Menu Bar
with dpg.viewport_menu_bar():
    with dpg.menu(label="Tools"):
        dpg.add_menu_item(label="Open Defending Unit", callback=lambda: dpg.show_item(defending_window_tag))
        dpg.add_menu_item(label="Open Simple Attack Tool", callback=lambda: dpg.show_item(saw_tag))

# Start GUI
dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()