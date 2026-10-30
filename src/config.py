import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/screen-matrix")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "lang": "en",                       # "en" (default) or "zh"
    "mode": 1,                          # 1: Dual Linux Mint, 2: Barrier Share, 3: Moonlight Stream
    "secondary_position": "right",      # "right" or "left" (relative to Ultrawide Windows display)
    "mac_position": "right",            # Legacy alias
    "mode3_audio": "windows_only",      # "windows_only", "mac_only", "both"
    "capture_win_key": True,            # True: forward Win key to Windows, False: keep on Linux Mint
    "windows_ip": "192.168.1.100",      # Windows host IP
    "ultrawide_res": "3440x1440",       # Ultrawide native resolution
    "ultrawide_rate": "60",             # Ultrawide refresh rate
    "secondary_res": "2560x1600",       # Linux Mint display resolution
    "secondary_rate": "59.97"           # Linux Mint display refresh rate
}

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                # Keep compatibility between secondary_position and mac_position
                if "mac_position" in data and "secondary_position" not in data:
                    config["secondary_position"] = data["mac_position"]
                elif "secondary_position" in data:
                    config["mac_position"] = data["secondary_position"]
                return config
        except Exception as e:
            print(f"[Config] Error loading config: {e}, falling back to defaults")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        # Sync alias
        if "secondary_position" in config:
            config["mac_position"] = config["secondary_position"]
        elif "mac_position" in config:
            config["secondary_position"] = config["mac_position"]
            
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Config] Error saving config: {e}")
        return False
