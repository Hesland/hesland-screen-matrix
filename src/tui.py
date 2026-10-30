import os
import sys
from .config import load_config, save_config, normalize_mode
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
        cur_mode = normalize_mode(cfg.get("mode"))
        cur_pos = cfg.get("secondary_position", cfg.get("mac_position", "right")).upper()
        cur_audio = cfg.get("mode3_audio", "windows_only")
        cur_win = cfg.get("capture_win_key", True)
        cur_lang = cfg.get("lang", "en").upper()

        m1_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == "linux-only" else "        "
        m2_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == "linux-win" else "        "
        m3_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == "win-only" else "        "
        m4_tag = f"{C_GREEN}{C_BOLD}[ACTIVE]{C_RESET}" if cur_mode == "terminal-only" else "        "

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
        print(f"║  {C_BOLD}[1]{C_RESET} linux-only   : Linux Mint Native Dual-Screen (3440x1440)      {m1_tag}  ║")
        print(f"║  {C_BOLD}[2]{C_RESET} linux-win    : Native Dual-OS KVM (Windows 240Hz + Barrier)   {m2_tag}  ║")
        print(f"║  {C_BOLD}[3]{C_RESET} win-only     : Windows Extended Display (Stream to Mint)      {m3_tag}  ║")
        print(f"║  {C_BOLD}[4]{C_RESET} terminal-only: Pure Linux Terminal Companion (Shared Clip)     {m4_tag}  ║")
        print(f"{C_BLUE}{C_BOLD}╠════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"║  {C_BOLD}Placement{C_RESET}    :  {pos_r}   /   {pos_l}                                ║")
        print(f"║  {C_BOLD}win-only Aud{C_RESET} :  {aud_str}                     ║")
        print(f"║  {C_BOLD}Win Key Fwd{C_RESET}  :  {win_str}                                        ║")
        print(f"║  {C_BOLD}Language{C_RESET}     :  [G] {cur_lang} (Toggle English / 中文)                             ║")
        print(f"{C_BLUE}{C_BOLD}╠════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
        print(f"║  {C_MAGENTA}Actions:{C_RESET} [C] Cycle Modes  |  [T] Toggle 1&2  |  [S] Status  |  [Q] Quit    ║")
        print(f"{C_BLUE}{C_BOLD}╚════════════════════════════════════════════════════════════════════════════╝{C_RESET}")

        try:
            choice = input(f"{C_BOLD}Select an option > {C_RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting ScreenMatrix TUI. Goodbye!")
            break

        if choice in ["q", "exit", "quit"]:
            print("Exiting ScreenMatrix TUI.")
            break
        elif choice in ["1", "linux-only", "linux"]:
            apply_mode("linux-only", cfg)
        elif choice in ["2", "linux-win", "kvm"]:
            apply_mode("linux-win", cfg)
        elif choice in ["3", "win-only", "win"]:
            apply_mode("win-only", cfg)
        elif choice in ["4", "terminal-only", "term", "terminal"]:
            apply_mode("terminal-only", cfg)
        elif choice in ["r", "right"]:
            cfg["secondary_position"] = "right"
            cfg["mac_position"] = "right"
            save_config(cfg)
            if cfg.get("mode") in ["linux-only", "linux-win", "terminal-only"]:
                apply_mode(cfg.get("mode"), cfg)
        elif choice in ["l", "left"]:
            cfg["secondary_position"] = "left"
            cfg["mac_position"] = "left"
            save_config(cfg)
            if cfg.get("mode") in ["linux-only", "linux-win", "terminal-only"]:
                apply_mode(cfg.get("mode"), cfg)
        elif choice in ["w", "win"]:
            cfg["mode3_audio"] = "windows_only"
            save_config(cfg)
            if cfg.get("mode") == "win-only":
                apply_mode("win-only", cfg)
        elif choice in ["b", "both"]:
            cfg["mode3_audio"] = "both"
            save_config(cfg)
            if cfg.get("mode") == "win-only":
                apply_mode("win-only", cfg)
        elif choice in ["m", "mint"]:
            cfg["mode3_audio"] = "mac_only"
            save_config(cfg)
            if cfg.get("mode") == "win-only":
                apply_mode("win-only", cfg)
        elif choice in ["k", "key"]:
            cfg["capture_win_key"] = not cfg.get("capture_win_key", True)
            save_config(cfg)
            if cfg.get("mode") == "win-only":
                apply_mode("win-only", cfg)
        elif choice in ["g", "lang"]:
            cfg["lang"] = "zh" if cfg.get("lang") == "en" else "en"
            save_config(cfg)
        elif choice in ["c", "cycle"]:
            cycle_mode()
        elif choice in ["t", "toggle"]:
            cur = normalize_mode(cfg.get("mode"))
            next_m = "linux-win" if cur == "linux-only" else "linux-only"
            apply_mode(next_m, cfg)
        elif choice in ["s", "status"]:
            import json
            print(json.dumps(cfg, indent=4, ensure_ascii=False))
            input("\nPress Enter to continue...")

def main():
    render_tui()

if __name__ == "__main__":
    main()
