import os
import sys
from .config import load_config, save_config
from .core import apply_mode, cycle_mode
from .i18n import t

# ANSI Colors
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GREEN = "\033[32m"
C_BLUE = "\033[34m"
C_CYAN = "\033[36m"
C_YELLOW = "\033[33m"
C_MAGENTA = "\033[35m"
C_WHITE = "\033[37m"

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def render_tui():
    while True:
        cfg = load_config()
        cur_mode = cfg.get("mode", 1)
        cur_pos = cfg.get("secondary_position", cfg.get("mac_position", "right")).upper()
        cur_audio = cfg.get("mode3_audio", "windows_only")
        cur_win = cfg.get("capture_win_key", True)
        cur_lang = cfg.get("lang", "en").upper()

        m1_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == 1 else "        "
        m2_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == 2 else "        "
        m3_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == 3 else "        "

        pos_r = f"{C_CYAN}{C_BOLD}[R] Right (*){C_RESET}" if cur_pos == "RIGHT" else "[R] Right"
        pos_l = f"{C_CYAN}{C_BOLD}[L] Left (*){C_RESET}" if cur_pos == "LEFT" else "[L] Left"

        if cur_audio == "windows_only":
            aud_str = f"{C_YELLOW}{C_BOLD}[W] Windows Only (*){C_RESET} | [B] Both | [M] Linux Mint"
        elif cur_audio == "both":
            aud_str = f"[W] Windows Only | {C_YELLOW}{C_BOLD}[B] Both (*){C_RESET} | [M] Linux Mint"
        else:
            aud_str = f"[W] Windows Only | [B] Both | {C_YELLOW}{C_BOLD}[M] Linux Mint (*){C_RESET}"

        win_str = f"{C_GREEN}{C_BOLD}[K] Enabled (Always){C_RESET}" if cur_win else f"{C_WHITE}[K] Disabled (Never){C_RESET}"

        clear_screen()
        print(f"{C_BLUE}{C_BOLD}╔════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_BLUE}{C_BOLD}║              🖥️  Hesland ScreenMatrix (Terminal-Only TUI)                  ║{C_RESET}")
        print(f"{C_BLUE}{C_BOLD}║      Cross-System Dual-PC Display Synergy Hub for Linux Mint + Windows     ║{C_RESET}")
        print(f"{C_BLUE}{C_BOLD}╠════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"║  {C_BOLD}[1]{C_RESET} Mode 1: Linux Mint Native Dual-Screen (3440x1440 60Hz)      {m1_tag}  ║")
        print(f"║  {C_BOLD}[2]{C_RESET} Mode 2: Native Dual-OS KVM (Windows 240Hz + Barrier)        {m2_tag}  ║")
        print(f"║  {C_BOLD}[3]{C_RESET} Mode 3: Linux Mint as Windows Extended Display (Stream)     {m3_tag}  ║")
        print(f"{C_BLUE}{C_BOLD}╠════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"║  {C_BOLD}Placement{C_RESET}   :  {pos_r}   /   {pos_l}                                ║")
        print(f"║  {C_BOLD}Mode 3 Audio{C_RESET}:  {aud_str}                     ║")
        print(f"║  {C_BOLD}Win Key Fwd{C_RESET} :  {win_str}                                        ║")
        print(f"║  {C_BOLD}Language{C_RESET}    :  [G] {cur_lang} (Toggle English / 中文)                             ║")
        print(f"{C_BLUE}{C_BOLD}╠════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"║  {C_MAGENTA}Actions:{C_RESET} [C] Cycle Mode  |  [T] Toggle Mode 1&2  |  [S] Status  |  [Q] Quit ║")
        print(f"{C_BLUE}{C_BOLD}╚════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

        try:
            choice = input(f"{C_BOLD}Select an option > {C_RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting ScreenMatrix TUI. Goodbye!")
            break

        if choice in ["q", "exit", "quit"]:
            print("Exiting ScreenMatrix TUI.")
            break
        elif choice == "1":
            cfg["mode"] = 1
            apply_mode(1, cfg)
        elif choice == "2":
            cfg["mode"] = 2
            apply_mode(2, cfg)
        elif choice == "3":
            cfg["mode"] = 3
            apply_mode(3, cfg)
        elif choice in ["r", "right"]:
            cfg["secondary_position"] = "right"
            cfg["mac_position"] = "right"
            save_config(cfg)
            if cfg.get("mode") in [1, 2]:
                apply_mode(cfg.get("mode"), cfg)
        elif choice in ["l", "left"]:
            cfg["secondary_position"] = "left"
            cfg["mac_position"] = "left"
            save_config(cfg)
            if cfg.get("mode") in [1, 2]:
                apply_mode(cfg.get("mode"), cfg)
        elif choice in ["w", "win"]:
            cfg["mode3_audio"] = "windows_only"
            save_config(cfg)
            if cfg.get("mode") == 3:
                apply_mode(3, cfg)
        elif choice in ["b", "both"]:
            cfg["mode3_audio"] = "both"
            save_config(cfg)
            if cfg.get("mode") == 3:
                apply_mode(3, cfg)
        elif choice in ["m", "mint"]:
            cfg["mode3_audio"] = "mac_only"
            save_config(cfg)
            if cfg.get("mode") == 3:
                apply_mode(3, cfg)
        elif choice in ["k", "key"]:
            cfg["capture_win_key"] = not cfg.get("capture_win_key", True)
            save_config(cfg)
            if cfg.get("mode") == 3:
                apply_mode(3, cfg)
        elif choice in ["g", "lang"]:
            cfg["lang"] = "zh" if cfg.get("lang") == "en" else "en"
            save_config(cfg)
        elif choice in ["c", "cycle"]:
            cycle_mode()
        elif choice in ["t", "toggle"]:
            cur = cfg.get("mode", 1)
            apply_mode(2 if cur == 1 else 1, cfg)
        elif choice in ["s", "status"]:
            import json
            print(json.dumps(cfg, indent=4, ensure_ascii=False))
            input("\nPress Enter to continue...")

def main():
    render_tui()

if __name__ == "__main__":
    main()
