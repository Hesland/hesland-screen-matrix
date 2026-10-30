import os
import subprocess
import time
from .config import load_config, save_config
from .i18n import t

def run_cmd(cmd, env=None, background=False):
    full_env = os.environ.copy()
    full_env.setdefault("DISPLAY", ":0")
    full_env.setdefault("XAUTHORITY", os.path.expanduser("~/.Xauthority"))
    full_env.setdefault("QT_QPA_PLATFORM", "xcb")
    full_env.setdefault("LD_LIBRARY_PATH", "/home/hesland/.local/barrier/usr/lib:/home/hesland/.local/barrier/usr/lib/x86_64-linux-gnu")
    if env:
        full_env.update(env)
    
    if background:
        return subprocess.Popen(cmd, shell=True, env=full_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        res = subprocess.run(cmd, shell=True, env=full_env, capture_output=True, text=True)
        return res

def notify(title, message, icon="video-display", timeout=3500):
    cmd = f'notify-send -t {timeout} -i "{icon}" "{title}" "{message}"'
    run_cmd(cmd)

def get_target_port():
    res = run_cmd("xrandr | grep ' connected' | grep -v 'eDP-1' | awk '{print $1}' | head -n 1")
    port = res.stdout.strip()
    return port if port else "DP-1"

def notify_windows(mode_num, win_ip="192.168.1.100"):
    cmd = f'ssh -o ConnectTimeout=2 -o BatchMode=yes hesland@{win_ip} "powershell -ExecutionPolicy Bypass -File C:/Users/Hesland/set_win_mode.ps1 -Mode {mode_num}"'
    run_cmd(cmd, background=True)

def generate_barrier_conf(pos="right", cfg=None):
    conf_dir = os.path.expanduser("~/.config/barrier")
    os.makedirs(conf_dir, exist_ok=True)
    conf_path = os.path.join(conf_dir, "barrier.conf")
    
    if pos == "right":
        links = """    hesland-MacBookPro:
        left = HESLAND-R5-5600
    HESLAND-R5-5600:
        right = hesland-MacBookPro"""
        tip = t("slide_tip_right", cfg)
    else:
        links = """    hesland-MacBookPro:
        right = HESLAND-R5-5600
    HESLAND-R5-5600:
        left = hesland-MacBookPro"""
        tip = t("slide_tip_left", cfg)

    content = f"""section: screens
    hesland-MacBookPro:
    HESLAND-R5-5600:
end

section: links
{links}
end

section: options
    relativeMouseMoves = false
    screenSaverSync = false
    win32KeepForeground = false
    clipboardSharing = true
    switchCorners = none
    switchCornerSize = 0
    keystroke(Control+Alt+s) = switchToScreen(HESLAND-R5-5600)
    keystroke(Control+Alt+a) = switchToScreen(hesland-MacBookPro)
end
"""
    with open(conf_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    pos_file = os.path.join(conf_dir, "mac_position")
    with open(pos_file, "w", encoding="utf-8") as f:
        f.write(pos)
        
    return tip

def apply_mode_1(cfg=None):
    if cfg is None:
        cfg = load_config()
    cfg["mode"] = 1
    save_config(cfg)
    
    run_cmd("pkill -f barrier_daemon.sh || true; pkill -f barriers || true; systemctl --user stop barriers-server.service 2>/dev/null || true")
    run_cmd("pkill -f moonlight || true; pkill -f Moonlight.AppImage || true")
    
    notify_windows(1, cfg.get("windows_ip", "192.168.1.100"))
    
    target_port = get_target_port()
    pos = cfg.get("secondary_position", cfg.get("mac_position", "right"))
    
    # Keep 100% in sync with Cinnamon monitors config
    if pos == "right":
        xrandr_cmd = (
            f"xrandr --output {target_port} --primary --mode {cfg.get('ultrawide_res', '3440x1440')} --rate {cfg.get('ultrawide_rate', '60')} --pos 0x0 "
            f"--output eDP-1 --mode {cfg.get('secondary_res', '2560x1600')} --rate {cfg.get('secondary_rate', '59.97')} --pos 3440x0"
        )
    else:
        xrandr_cmd = (
            f"xrandr --output eDP-1 --mode {cfg.get('secondary_res', '2560x1600')} --rate {cfg.get('secondary_rate', '59.97')} --pos 0x0 "
            f"--output {target_port} --primary --mode {cfg.get('ultrawide_res', '3440x1440')} --rate {cfg.get('ultrawide_rate', '60')} --pos 2560x0"
        )
    
    res = run_cmd(xrandr_cmd)
    if res.returncode != 0:
        if pos == "right":
            run_cmd(f"xrandr --output {target_port} --primary --auto --left-of eDP-1 --output eDP-1 --auto")
        else:
            run_cmd(f"xrandr --output {target_port} --primary --auto --right-of eDP-1 --output eDP-1 --auto")
            
    mode_file = os.path.expanduser("~/.screenlayout/current_mode")
    with open(mode_file, "w") as f:
        f.write("1\n")
        
    notify(t("notif_m1_title", cfg), t("notif_m1_msg", cfg), "video-display")

def apply_mode_2(cfg=None):
    if cfg is None:
        cfg = load_config()
    cfg["mode"] = 2
    save_config(cfg)
    
    run_cmd("pkill -f moonlight || true; pkill -f Moonlight.AppImage || true")
    
    target_port = get_target_port()
    run_cmd(f"xrandr --output {target_port} --off")
    run_cmd(f"xrandr --output eDP-1 --primary --mode {cfg.get('secondary_res', '2560x1600')} --rate {cfg.get('secondary_rate', '59.97')}")
    
    pos = cfg.get("secondary_position", cfg.get("mac_position", "right"))
    tip = generate_barrier_conf(pos, cfg)
    
    run_cmd("systemctl --user restart barriers-server.service 2>/dev/null || { pkill -f barriers || true; ~/.config/barrier/start_server.sh; }")
    notify_windows(2, cfg.get("windows_ip", "192.168.1.100"))
    
    mode_file = os.path.expanduser("~/.screenlayout/current_mode")
    with open(mode_file, "w") as f:
        f.write("2\n")
        
    pos_desc = "RIGHT" if pos == "right" else "LEFT"
    if cfg.get("lang") == "zh":
        pos_desc = "右侧" if pos == "right" else "左侧"
        
    notify(t("notif_m2_title", cfg), t("notif_m2_msg", cfg, pos=pos_desc, tip=tip), "input-keyboard")

def apply_mode_3(cfg=None):
    if cfg is None:
        cfg = load_config()
    cfg["mode"] = 3
    save_config(cfg)
    
    run_cmd("pkill -f barrier_daemon.sh || true; pkill -f barriers || true; systemctl --user stop barriers-server.service 2>/dev/null || true")
    run_cmd("pkill -f moonlight || true; pkill -f Moonlight.AppImage || true")
    
    target_port = get_target_port()
    run_cmd(f"xrandr --output {target_port} --off")
    run_cmd(f"xrandr --output eDP-1 --primary --mode {cfg.get('secondary_res', '2560x1600')} --rate {cfg.get('secondary_rate', '59.97')}")
    
    notify_windows(3, cfg.get("windows_ip", "192.168.1.100"))
    time.sleep(0.5)
    
    env = {}
    extra_args = []
    
    audio_policy = cfg.get("mode3_audio", "windows_only")
    if audio_policy == "windows_only":
        env["SDL_AUDIODRIVER"] = "dummy"
        extra_args.append("--audio-on-host")
        audio_tip = t("audio_tip_win", cfg)
    elif audio_policy == "both":
        extra_args.append("--audio-on-host")
        audio_tip = t("audio_tip_both", cfg)
    else:
        audio_tip = t("audio_tip_mint", cfg)
        
    capture_win = cfg.get("capture_win_key", True)
    if capture_win:
        extra_args.append("--capture-system-keys always")
        key_tip = t("key_tip_on", cfg)
    else:
        extra_args.append("--capture-system-keys never")
        key_tip = t("key_tip_off", cfg)
        
    moonlight_bin = os.path.expanduser("~/Applications/Moonlight.AppImage")
    win_ip = cfg.get("windows_ip", "192.168.1.100")
    stream_cmd = (
        f'nohup "{moonlight_bin}" stream {win_ip} Desktop --resolution {cfg.get("secondary_res", "2560x1600")} --fps 60 '
        f'--display-mode fullscreen {" ".join(extra_args)} >/dev/null 2>&1 &'
    )
    
    run_cmd(stream_cmd, env=env, background=True)
    
    mode_file = os.path.expanduser("~/.screenlayout/current_mode")
    with open(mode_file, "w") as f:
        f.write("3\n")
        
    notify(t("notif_m3_title", cfg), t("notif_m3_msg", cfg, audio_tip=audio_tip, key_tip=key_tip), "video-display")

def cycle_mode():
    cfg = load_config()
    cur = cfg.get("mode", 1)
    next_mode = 2 if cur == 1 else (3 if cur == 2 else 1)
    apply_mode(next_mode, cfg)

def apply_mode(mode_num, cfg=None):
    if cfg is None:
        cfg = load_config()
    if mode_num == 1:
        apply_mode_1(cfg)
    elif mode_num == 2:
        apply_mode_2(cfg)
    elif mode_num == 3:
        apply_mode_3(cfg)
