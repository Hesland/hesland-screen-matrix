import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/screen-matrix")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Mode mapping between numbers and semantic names
MODE_MAP_NUM_TO_NAME = {
    1: "linux-only",
    2: "linux-win",
    3: "win-only",
    4: "terminal-only"
}

MODE_MAP_NAME_TO_NUM = {
    "linux-only": 1,
    "linux-win": 2,
    "win-only": 3,
    "terminal-only": 4
}

DEFAULT_CONFIG = {
    "lang": "en",                       # "en" (default) or "zh"
    "mode": "linux-only",               # "linux-only", "linux-win", "win-only", "terminal-only"
    "secondary_position": "right",      # "right" or "left" (relative to Ultrawide display)
    "mac_position": "right",            # Legacy alias
    "mode3_audio": "windows_only",      # "windows_only", "mac_only", "both"
    "capture_win_key": True,            # True: forward Win key to Windows, False: keep on Linux Mint
    "windows_ip": "192.168.1.100",      # Windows host IP
    "ultrawide_res": "3440x1440",       # Ultrawide native resolution
    "ultrawide_rate": "60",             # Ultrawide refresh rate
    "secondary_res": "2560x1600",       # Linux Mint display resolution
    "secondary_rate": "59.97"           # Linux Mint display refresh rate
}

def normalize_mode(mode_val):
    if isinstance(mode_val, int):
        return MODE_MAP_NUM_TO_NAME.get(mode_val, "linux-only")
    if isinstance(mode_val, str):
        mode_str = mode_val.strip().lower()
        if mode_str in MODE_MAP_NAME_TO_NUM:
            return mode_str
        if mode_str.isdigit() and int(mode_str) in MODE_MAP_NUM_TO_NAME:
            return MODE_MAP_NUM_TO_NAME[int(mode_str)]
        aliases = {
            "linux": "linux-only",
            "win": "win-only",
            "kvm": "linux-win",
            "term": "terminal-only",
            "terminal": "terminal-only"
        }
        if mode_str in aliases:
            return aliases[mode_str]
    return "linux-only"

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                config["mode"] = normalize_mode(config.get("mode"))
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
        if "secondary_position" in config:
            config["mac_position"] = config["secondary_position"]
        elif "mac_position" in config:
            config["secondary_position"] = config["mac_position"]
            
        config["mode"] = normalize_mode(config.get("mode"))
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Config] Error saving config: {e}")
        return False
