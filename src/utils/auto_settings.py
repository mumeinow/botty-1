import json
import os
from config import Config
from mss import mss


def adjust_settings():
    # You might not belive it, but there are cases where users press f9 and just dont read any console output and think everything is done
    # so for now, removing this warning as it seems there has never been anybody actually backing up the original settings anyway...
    # print("Warning: This will overwrite some of your graphics and gameplay settings. D2R must not be running during this action! Continue with Enter...")
    # input()
    # find monitor res
    config = Config()
    sct = mss()
    monitor_idx = config.general["monitor"] + 1 # sct saves the whole screen (including both monitors if available at index 0, then monitor 1 at 1 and 2 at 2)
    if len(sct.monitors) == 1:
        print("How do you not have a monitor connected?!")
        os._exit(1)
    if monitor_idx >= len(sct.monitors):
        monitor_idx = 1
    monitor_res = f"{sct.monitors[monitor_idx]['width']}_{sct.monitors[monitor_idx]['height']}"
    # Get D2r folder
    d2_saved_games = f"C:\\Users\\{os.getlogin()}\\Saved Games\\Diablo II Resurrected"
    if not os.path.exists(d2_saved_games):
        print(f"Your D2R Saved Games folder could not be found here: {d2_saved_games}, input the correct location:")
        d2_saved_games = input()
    if not os.path.exists(d2_saved_games):
        assert(f"Could not find D2R Saved Games at {d2_saved_games}")
    # adjust settings
    f = open(d2_saved_games + "\\Settings.json")
    curr_settings = json.load(f)
    f = open("assets/d2r_settings.json")
    new_settings = json.load(f)
    for key in new_settings:
        curr_settings[key] = new_settings[key]
    # catch error where user sets a higher botty res than the monitor
    if monitor_res == "1280_720" and config.general["res"] == "1920_1080":
        print("ERROR: You can not set 'res' to 1920_1080 while your monitor is in 1280_720")
        return
    # In case monitor res is at 720p, force fullscreen
    if monitor_res == config.general["res"]:
        print(f"Detected param res and monitor res to be the same ({monitor_res}). Forcing fullscreen mode.")
        curr_settings["Window Mode"] = 1
        if monitor_res == "1920_1080":
            # most template screenshots where take with this setting in 1080p:
            curr_settings["Anti Aliasing"] = 1
    # write back to settings.json
    with open(d2_saved_games + "\\Settings.json", 'w') as outfile:
        json.dump(curr_settings, outfile)
    print("Changed settings succesfully. You can now start D2R and botty.")


if __name__ == "__main__":
    adjust_settings()
