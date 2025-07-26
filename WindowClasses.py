import dearpygui.dearpygui as dpg
import UnitClass as uc
import json
import os
import shutil

SAVE_DIR = "unit_saves"  # Subfolder for save files


class DefendingUnitWindow:
    def __init__(self, window_id: str, unit_name_map: dict, terrain_list: list, type_list: list):
        self.window_id = window_id
        self.group_id = f"{window_id}_group"
        self.unit_count = 1
        self.unit_name_map = unit_name_map
        self.terrain_list = terrain_list
        self.type_list = type_list
        self._create_window()

    def _tag(self, name):
        return f"{self.window_id}_{name}_{self.unit_count}"

    def _create_window(self):
        with dpg.window(label="Defending Unit", tag=self.window_id):
            with dpg.group(tag=self.group_id):
                dpg.add_text("Defending units:")
                self.add_unit_group()
            dpg.add_button(label="+", callback=self.add_callback)
            dpg.add_button(label="Save", callback=self.save_callback)
            dpg.add_button(label="Load", callback=self.load_callback)
            dpg.add_button(label="Clear All Saves", callback=self.clear_all_saves)

    def add_callback(self):
        self.add_unit_group()

    def add_type_group(self, preset=None):
        tag_suffix = self.unit_count

        # Determine initial label text and combo selection
        if preset:
            label_text = preset.get("label_text", "Unknown")
            combo_value = preset.get("combo_value", None)
            checkbox_value = preset.get("checkbox_value", False)
        else:
            label_text = "Unknown"
            combo_value = None
            checkbox_value = False

        def change_type():
            if dpg.is_item_visible(f"{self.group_id}_sub_group_{tag_suffix}_label"):
                dpg.hide_item(f"{self.group_id}_sub_group_{tag_suffix}_label")
                dpg.show_item(f"{self.group_id}_sub_group_{tag_suffix}_combo")
            else:
                dpg.show_item(f"{self.group_id}_sub_group_{tag_suffix}_label")
                dpg.hide_item(f"{self.group_id}_sub_group_{tag_suffix}_combo")

        with dpg.group(parent=f"{self.group_id}_sub_group_{tag_suffix}", horizontal=True):
            dpg.add_text("Type:")
            dpg.add_text(label_text, tag=f"{self.group_id}_sub_group_{tag_suffix}_label")
            dpg.add_combo(items=self.type_list, tag=f"{self.group_id}_sub_group_{tag_suffix}_combo", width=100, default_value=combo_value)
            dpg.add_text("Override type:")
            dpg.add_checkbox(tag=f"{self.group_id}_sub_group_{tag_suffix}_checkbox", default_value=checkbox_value, callback=change_type)

        # Set initial visibility based on checkbox
        if checkbox_value:
            dpg.hide_item(f"{self.group_id}_sub_group_{tag_suffix}_label")
            dpg.show_item(f"{self.group_id}_sub_group_{tag_suffix}_combo")
        else:
            dpg.show_item(f"{self.group_id}_sub_group_{tag_suffix}_label")
            dpg.hide_item(f"{self.group_id}_sub_group_{tag_suffix}_combo")
            
            

    def add_unit_group(self, preset=None):
        tag_suffix = self.unit_count
        with dpg.group(parent=self.group_id, horizontal=True, id=f"{self.group_id}_sub_group_{tag_suffix}" ):
            dpg.add_text(f"Unit {tag_suffix}:")
            dpg.add_combo(items=list(self.unit_name_map.keys()), tag=self._tag("unit_combo"), width=250,
                        default_value=preset["unit_name"] if preset else None, callback=self.update_data)
            dpg.add_spacer()
            dpg.add_text("Amount:")
            dpg.add_input_int(tag=self._tag("unit_amount"), width=80,
                            default_value=preset["amount"] if preset else 0)
            dpg.add_spacer()

            # Prepare the type preset
            type_preset = None
            if preset:
                type_preset = {
                                "label_text": preset.get("label_text", getattr(self.unit_name_map.get(preset["unit_name"], {}), "type", "Unknown")),
                                "combo_value": preset.get("type_override_value", None),
                                "checkbox_value": preset.get("type_override_checked", False)
                            }

            self.add_type_group(type_preset)

            dpg.add_spacer()
            dpg.add_text("Terrain:")
            dpg.add_combo(items=self.terrain_list, tag=self._tag("terrain"), width=100,
                        default_value=preset["terrain"] if preset else "open")
            dpg.add_spacer()
            dpg.add_text("Additional defence buff:")
            dpg.add_input_int(tag=self._tag("unit_buff"), width=80,
                            default_value=preset["buff"] if preset else 0)
            dpg.add_text("%")
            dpg.add_spacer()
            dpg.add_text("Health:")
            dpg.add_input_float(tag=self._tag("unit_health"), width=100,
                    default_value=preset.get("health", 100) if preset else 100)
            dpg.add_text("/")
            dpg.add_input_float(tag=self._tag("unit_max_health"), width=100,
                                default_value=preset.get("max_health", 100) if preset else 100)

        self.unit_count += 1

    def update_data(self):
        for i in range(1, self.unit_count):
            try:
                unit_name = dpg.get_value(f"{self.window_id}_unit_combo_{i}")
            except Exception:
                continue

            if unit_name not in self.unit_name_map:
                continue

            unit = self.unit_name_map[unit_name]
            # Assuming unit has a 'type' attribute; adjust if different
            unit_type = getattr(unit, "type", "Unknown")

            # Update the text label for the type display
            label_tag = f"{self.group_id}_sub_group_{i}_label"
            if dpg.does_item_exist(label_tag):
                dpg.set_value(label_tag, f"{unit_type}")

    def save_callback(self):
        data = []

        for i in range(1, self.unit_count):
            try:
                unit_name = dpg.get_value(f"{self.window_id}_unit_combo_{i}")
                amount = dpg.get_value(f"{self.window_id}_unit_amount_{i}")
                terrain = dpg.get_value(f"{self.window_id}_terrain_{i}")
                buff = dpg.get_value(f"{self.window_id}_unit_buff_{i}")
                health = dpg.get_value(f"{self.window_id}_unit_health_{i}")
                max_health = dpg.get_value(f"{self.window_id}_unit_max_health_{i}")

                type_override_checked = dpg.get_value(f"{self.group_id}_sub_group_{i}_checkbox")
                type_override_value = dpg.get_value(f"{self.group_id}_sub_group_{i}_combo")
                label_text = dpg.get_value(f"{self.group_id}_sub_group_{i}_label")
            except Exception:
                continue

            if unit_name not in self.unit_name_map:
                continue

            unit = self.unit_name_map[unit_name]

            data.append({
                "unit": unit.to_dict(),
                "amount": amount,
                "defence_buff": buff,
                "terrain": terrain,
                "health": health,
                "max_health": max_health,
                "type_override_checked": type_override_checked,
                "type_override_value": type_override_value,
                "label_text": label_text,
                "type": type_override_value if type_override_checked else getattr(unit, "type", "Unknown")
            })

        os.makedirs(SAVE_DIR, exist_ok=True)
        filename = os.path.join(SAVE_DIR, f"{self.window_id}_units.json")
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {filename}")

    def load_callback(self):
        filename = os.path.join(SAVE_DIR, f"{self.window_id}_units.json")
        if not os.path.exists(filename):
            print("No saved file found.")
            return

        with open(filename, "r") as f:
            data = json.load(f)

        dpg.delete_item(self.group_id, children_only=True)
        dpg.add_text("Defending units:", parent=self.group_id)
        self.unit_count = 1

        for entry in data:
            unit_data = entry["unit"]
            self.add_unit_group(preset={
                "unit_name": unit_data["name"],
                "amount": entry["amount"],
                "buff": entry["defence_buff"],
                "terrain": entry.get("terrain", "open"),
                "health": entry.get("health", 100),
                "max_health": entry.get("max_health", 100),
                "type_override_checked": entry.get("type_override_checked", False),
                "type_override_value": entry.get("type_override_value", None),
                "label_text": entry.get("label_text", entry.get("type", unit_data.get("type", "Unknown")))
            })
            print(f"Loaded from {filename}")

    
    def clear_all_saves(self):
        if os.path.exists(SAVE_DIR):
            for filename in os.listdir(SAVE_DIR):
                file_path = os.path.join(SAVE_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"All files in '{SAVE_DIR}' have been deleted.")
        else:
            print(f"No save directory '{SAVE_DIR}' found.")


class SimpleAttackWindow:
    def __init__(self, window_id: str, unit_name_map: dict, terrain_list: list, type_list: list):
        self.window_id = window_id
        self.group_id = f"{window_id}_group"
        self.unit_count = 1
        self.unit_name_map = unit_name_map
        self.terrain_list = terrain_list
        self.type_list = type_list
        self._create_window()

    def _tag(self, name):
        return f"{self.window_id}_{name}_{self.unit_count}"

    def type_group(self, type):
        with dpg.group(tag=f"{self.group_id}_{type}", horizontal=True):
                dpg.add_text(f"Damage to type: {type}")
                dpg.add_input_float(tag=f"{self.group_id}_{type}_damage" ,width=100)

    def simulate_single_attack(self):
        dpg.delete_item(f"{self.group_id}_result")
        filename = os.path.join(SAVE_DIR, "defending_unit_window_units.json")  # Adjust if using a different window_id
        if not os.path.exists(filename):
            print("No saved defending units found.")
            return

        with open(filename, "r") as f:
            data = json.load(f)

        units = []

        for entry in data:
            while entry["amount"] >0:
                unit_data = entry["unit"]
                unit = uc.Unit.from_dict(unit_data, entry["type"], entry["defence_buff"] )

                # Override type if needed
                if entry.get("type_override_checked", False):
                    unit.type = entry.get("type_override_value", unit.type)

                units.append(unit)
                entry["amount"] -= 1

        print("Loaded defending units:")
        dmg_list = []
        for unit_type in self.type_list:
            damage = dpg.get_value(f"{self.group_id}_{unit_type}_damage")
            dmg_list.append(damage)


        simulator = uc.UnitDamage(units)

        result = simulator.simple_attack(dmg_list)
        with dpg.group(tag=f"{self.group_id}_result", parent=self.group_id):
            for i in result:
                dpg.add_text(f"{i[0]} recives {i[1]} damage")

        # Now `units` is a list of Unit instances ready for further simulation

    def _create_window(self):
        with dpg.window(label="Simple Attack Window", tag=self.window_id):
            with dpg.group(tag=self.group_id):
                for i in self.type_list:
                    self.type_group(i)
                dpg.add_button(label="Simulate single attack", callback=self.simulate_single_attack)
                dpg.add_text("----result under here----")