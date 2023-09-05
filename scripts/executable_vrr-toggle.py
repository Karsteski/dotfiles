#!/bin/python

import os
import sys
import argparse
import subprocess
import json
from typing import Optional

def parseArgument() -> Optional[bool]:
    """
    Get the argument (or lack thereof) passed by the user
    """

    description = "Toggle DP-1's Variable Refresh Rate(VRR)"

    # RawTextHelpFormatter indicates text is already wrapped and formatted
    parser = argparse.ArgumentParser(prog="VRR-Toggle",
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-t", "--toggle", type=int, default=None, required=False,
        choices=[0, 1],
        help="Select whether to use VRR")

    arguments = parser.parse_args()
    arg: Optional[bool] = arguments.toggle

    return arg

def getVRRStatus() -> bool:
    """
    Get the VRR Status of DP-1 via $ swaymsg ...
    """
    output = subprocess.check_output("swaymsg -r -t get_outputs", shell=True)
    output_string = output.decode(encoding="utf-8")
    json_output = json.loads(output_string)

    for entry in json_output:
        if entry["name"] == "DP-1":
            status: str = entry["adaptive_sync_status"]
            return status == "enabled"

    VRR_status = False
    return VRR_status


def toggleVRR(flag: bool) -> None:
    """
    Toggle Variable Refresh Rate via $ swaymsg ...
    """
    if flag:
        os.system("swaymsg 'output DP-1 adaptive_sync on'")
    else:
        os.system("swaymsg 'output DP-1 adaptive_sync off'")

def printJSON(use_VRR: bool) -> None:
    """
    For use by programs for Sway such as Waybar
    """

    if use_VRR:
        print('{"text": "󰍹", "tooltip": "VRR Enabled", "class": "enabled"}')
    else:
        print('{"text": "󰶐", "tooltip": "VRR Disabled", "class": "disabled"}')


if __name__ == "__main__":
    arg: Optional[bool] =  parseArgument()

    # If no argument provided, just print the last setting used
    if arg is None:
        printJSON(getVRRStatus())
        sys.exit()
    else:
        toggleVRR(arg)

    # Echo the flag so that a program like Waybar knows which option was selected
    printJSON(arg)