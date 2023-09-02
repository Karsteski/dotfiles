#!/bin/python
# flake8: noqa: E221

import os, argparse
from pathlib import Path
from enum import IntEnum 

MANGOHUD_CONFIG_PATH = str(Path.home()) + "/.config/MangoHud/MangoHud.conf"

class MangoHudPreset(IntEnum):  
    Disable                 = 0
    OnlyFps                 = 1
    ProcessorInfo           = 2
    Detailed                = 3


def parseArguments() -> MangoHudPreset:
    description = """Switch between multiple MangoHud presets:
    Disable                         = 0
    Only FPS                        = 1
    Processor Info                  = 2
    Detailed Statistics             = 3
    """
    
    parser = argparse.ArgumentParser(description=description, 
        formatter_class=argparse.RawTextHelpFormatter)

    # RawTextHelpFormatter indicates text is already wrapped and formatted
    parser.add_argument("preset", type=int, help="Select the MangoHud preset")
    
    arguments = parser.parse_args()
    preset : int = arguments.preset

    if preset not in [0, 1, 2, 3]:
        print("Invalid argument, please check help to see how to use this script")
        exit()
    
    return MangoHudPreset(preset)


def getCommonSettings() ->str:
    # Settings that are shared between the presets
    return """
background_alpha=0.1
font_size=20

toggle_hud=Shift_R+F12
    """

def getPresetString(level_of_detail: MangoHudPreset = MangoHudPreset.ProcessorInfo) -> str:
    disable = "no_display"

    only_fps = """
control=mangohud
fsr_steam_sharpness=5
nis_steam_sharpness=10
frame_timing=0
cpu_stats=0
gpu_stats=0
fps=1
fps_only
legacy_layout=0
width=40
frametime=0
    """

    processor_info = """
control=mangohud
fsr_steam_sharpness=5
nis_steam_sharpness=10
legacy_layout=0
background_alpha=0
horizontal
fps
gpu_stats
gpu_temp
cpu_stats
cpu_temp
ram
vram
fsr
frametime=0
hud_no_margin
table_columns=14
frame_timing=1
    """

    detailed = """
control=mangohud
fsr_steam_sharpness=5
nis_steam_sharpness=10
full
cpu_temp
gpu_temp
ram
vram
arch
gpu_name
cpu_power
gpu_power
wine
fsr
frametime
battery
    """
    
    match level_of_detail:
        case MangoHudPreset.Disable:
            return disable
        case MangoHudPreset.OnlyFps:
            return only_fps
        case MangoHudPreset.ProcessorInfo:
            return processor_info
        case MangoHudPreset.Detailed:
            return detailed


def writeConfig(config_path: str, config: str) -> bool:
    if os.path.exists(config_path):
        try:
            with open(config_path, "w") as file:
                file.write(config)

            return True
        except Exception as error:
            print("An exception occurred: ", error)
            return False
    else:
        print("File path does not exist: ", config_path)
        return False


if __name__ == "__main__":
    selected_preset = parseArguments()

    preset = getPresetString(selected_preset)

    full_settings = getCommonSettings() + preset
    was_write_successful = writeConfig(MANGOHUD_CONFIG_PATH, full_settings)

    if was_write_successful:
        # Echo the preset so that a program like Waybar knows which preset was selected
        print(int(selected_preset))
    else:
        # Error occurred 
        print(-1)
