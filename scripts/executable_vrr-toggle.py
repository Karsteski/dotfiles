#!/bin/python
"""
    This script toggles the Adaptive Sync (Variable Refresh Rate) setting
    via the Sway compositor. 
"""

import os
import argparse
import subprocess
import json
from typing import Any


def parseArguments(valid_displays: list[str]) -> tuple[str, bool]:
    """
    Get the arguments (or lack thereof) passed by the user
    Returns the name of the display and whether to toggle it
    """

    # RawTextHelpFormatter indicates text is already wrapped and formatted
    parser = argparse.ArgumentParser(
        prog="VRR-Toggle",
        description="Toggle a display's Variable Refresh Rate(VRR) setting via the Sway WM",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-t",
        "--toggle",
        action="store_true",
        required=False,
        help="Toggle Variable Refresh Rate",
    )

    parser.add_argument(
        "-d",
        "--display",
        required=True,
        choices=valid_displays,
        help="Select the display to use",
    )

    arguments = parser.parse_args()
    toggle: bool = arguments.toggle
    display: str = arguments.display

    return (display, toggle)


def getSwayMsgOutputJSON() -> dict[Any, Any]:
    """
    Retrieve the output of '$ swaymsg -r -t get_outputs' in a dict converted from JSON
    """
    output = subprocess.check_output("swaymsg -r -t get_outputs", shell=True)
    output_string = output.decode(encoding="utf-8")
    json_output: Any = json.loads(output_string)

    return json_output


def getOutputNames(sway_msg_output: dict[Any, Any]) -> list[str]:
    """
    Get the names of the display outputs via Sway WM
    Takes a dict of converted JSON data
    """

    output_names = []
    for entry in sway_msg_output:
        output_names.append(entry["name"])

    return output_names


def VRRStatus(output_display: str) -> bool:
    """
    Get the VRR Status of DP-1 via $ swaymsg ...
    """
    sway_outputs_JSON = subprocess.check_output("swaymsg -r -t get_outputs", shell=True)
    decoded_JSON = sway_outputs_JSON.decode(encoding="utf-8")
    json_output = json.loads(decoded_JSON)

    for entry in json_output:
        if entry["name"] == output_display:
            status: str = entry["adaptive_sync_status"]
            return status == "enabled"

    VRR_status = False
    return VRR_status


def toggleVRR(output_display: str, flag: bool) -> None:
    """
    Toggle Variable Refresh Rate via $ swaymsg ...
    """
    if flag:
        os.system(f"swaymsg 'output {output_display} adaptive_sync on'")
    else:
        os.system(f"swaymsg 'output {output_display} adaptive_sync off'")


def printJSON(output_display: str, using_VRR: bool) -> None:
    """
    Print JSON info for Waybar to use
    """

    # ensure_ascii flag will print in UTF-8 rather than ASCII
    if using_VRR:
        enabled_info = {
            "text": "󰍹",
            "tooltip": f"VRR Enabled: {output_display}",
            "class": "enabled",
        }
        json_data_enabled = json.dumps(enabled_info, ensure_ascii=False)
        print(json_data_enabled)
    else:
        disabled_info = {
            "text": "󰶐",
            "tooltip": f"VRR Disabled: {output_display}",
            "class": "disabled",
        }
        json_data_disabled = json.dumps(disabled_info, ensure_ascii=False)
        print(json_data_disabled)


if __name__ == "__main__":
    sway_msg_output = getSwayMsgOutputJSON()
    valid_displays = getOutputNames(sway_msg_output)

    display_name, toggle = parseArguments(valid_displays)
    status_VRR = VRRStatus(display_name)

    # Only toggle if requested, otherwise just print the current setting for use by Waybar
    if toggle:
        current_setting = VRRStatus(display_name)
        new_setting = not current_setting
        toggleVRR(display_name, new_setting)

    printJSON(display_name, status_VRR)
