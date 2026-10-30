import os
import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
    HAS_APP_INDICATOR = True
except Exception:
    HAS_APP_INDICATOR = False

from .config import load_config, save_config, normalize_mode
from .core import apply_mode, cycle_mode
from .i18n import t

APP_INDICATOR_ID = "screen_matrix_tray"

class ScreenMatrixTray:
    def __init__(self):
        self.config = load_config()
        self.menu = Gtk.Menu()
        self.build_menu()
        
        if HAS_APP_INDICATOR:
            self.indicator = AppIndicator.Indicator.new(
                APP_INDICATOR_ID,
                self.get_icon_name(),
                AppIndicator.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self.menu)
        else:
            self.status_icon = Gtk.StatusIcon.new_from_icon_name(self.get_icon_name())
            self.status_icon.connect("popup-menu", self.on_status_icon_popup)
            self.status_icon.set_tooltip_text("Hesland ScreenMatrix")

    def get_icon_name(self):
        mode = normalize_mode(self.config.get("mode"))
        if mode == "linux-only":
            return "video-display"
        elif mode == "linux-win":
            return "input-keyboard"
        elif mode == "win-only":
            return "preferences-desktop-display"
        else:
            return "utilities-terminal"

    def build_menu(self):
        for item in self.menu.get_children():
            self.menu.remove(item)

        cfg = self.config
        cur_mode = normalize_mode(cfg.get("mode"))
        cur_pos = cfg.get("secondary_position", cfg.get("mac_position", "right"))
        cur_audio = cfg.get("mode3_audio", "windows_only")
        cur_win_key = cfg.get("capture_win_key", True)
        cur_lang = cfg.get("lang", "en")

        # 1. 4 Modes Selection
        item_m1 = Gtk.MenuItem.new_with_label(f"{'● ' if cur_mode == 'linux-only' else '   '}{t('tray_linux_only', cfg)}")
        item_m1.connect("activate", lambda _: self.switch_mode("linux-only"))
        self.menu.append(item_m1)

        item_m2 = Gtk.MenuItem.new_with_label(f"{'● ' if cur_mode == 'linux-win' else '   '}{t('tray_linux_win', cfg)}")
        item_m2.connect("activate", lambda _: self.switch_mode("linux-win"))
        self.menu.append(item_m2)

        item_m3 = Gtk.MenuItem.new_with_label(f"{'● ' if cur_mode == 'win-only' else '   '}{t('tray_win_only', cfg)}")
        item_m3.connect("activate", lambda _: self.switch_mode("win-only"))
        self.menu.append(item_m3)

        item_m4 = Gtk.MenuItem.new_with_label(f"{'● ' if cur_mode == 'terminal-only' else '   '}{t('tray_terminal_only', cfg)}")
        item_m4.connect("activate", lambda _: self.switch_mode("terminal-only"))
        self.menu.append(item_m4)

        self.menu.append(Gtk.SeparatorMenuItem())

        # 2. Placement Submenu
        pos_menu_item = Gtk.MenuItem.new_with_label(t("tray_pos_menu", cfg))
        pos_submenu = Gtk.Menu()

        pos_right = Gtk.MenuItem.new_with_label(f"{'● ' if cur_pos == 'right' else '   '}{t('tray_pos_right', cfg)}")
        pos_right.connect("activate", lambda _: self.set_position("right"))
        pos_submenu.append(pos_right)

        pos_left = Gtk.MenuItem.new_with_label(f"{'● ' if cur_pos == 'left' else '   '}{t('tray_pos_left', cfg)}")
        pos_left.connect("activate", lambda _: self.set_position("left"))
        pos_submenu.append(pos_left)

        pos_menu_item.set_submenu(pos_submenu)
        self.menu.append(pos_menu_item)

        # 3. win-only Audio Submenu
        audio_menu_item = Gtk.MenuItem.new_with_label(t("tray_audio_menu", cfg))
        audio_submenu = Gtk.Menu()

        a_win = Gtk.MenuItem.new_with_label(f"{'● ' if cur_audio == 'windows_only' else '   '}{t('tray_audio_win', cfg)}")
        a_win.connect("activate", lambda _: self.set_audio("windows_only"))
        audio_submenu.append(a_win)

        a_both = Gtk.MenuItem.new_with_label(f"{'● ' if cur_audio == 'both' else '   '}{t('tray_audio_both', cfg)}")
        a_both.connect("activate", lambda _: self.set_audio("both"))
        audio_submenu.append(a_both)

        a_mint = Gtk.MenuItem.new_with_label(f"{'● ' if cur_audio == 'mac_only' else '   '}{t('tray_audio_mint', cfg)}")
        a_mint.connect("activate", lambda _: self.set_audio("mac_only"))
        audio_submenu.append(a_mint)

        audio_menu_item.set_submenu(audio_submenu)
        self.menu.append(audio_menu_item)

        # 4. Win Key Passthrough
        win_key_item = Gtk.CheckMenuItem.new_with_label(t("tray_win_key", cfg))
        win_key_item.set_active(cur_win_key)
        win_key_item.connect("toggled", self.toggle_win_key)
        self.menu.append(win_key_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        # 5. Language Switch Submenu
        lang_menu_item = Gtk.MenuItem.new_with_label(f"🌐 Language ({'English' if cur_lang == 'en' else '中文'})")
        lang_submenu = Gtk.Menu()

        l_en = Gtk.MenuItem.new_with_label(f"{'● ' if cur_lang == 'en' else '   '}English (Default)")
        l_en.connect("activate", lambda _: self.set_language("en"))
        lang_submenu.append(l_en)

        l_zh = Gtk.MenuItem.new_with_label(f"{'● ' if cur_lang == 'zh' else '   '}简体中文")
        l_zh.connect("activate", lambda _: self.set_language("zh"))
        lang_submenu.append(l_zh)

        lang_menu_item.set_submenu(lang_submenu)
        self.menu.append(lang_menu_item)

        # 6. Open GUI Control Panel
        gui_item = Gtk.MenuItem.new_with_label(t("tray_gui", cfg))
        gui_item.connect("activate", self.open_control_panel)
        self.menu.append(gui_item)

        # 7. Quit
        quit_item = Gtk.MenuItem.new_with_label(t("tray_quit", cfg))
        quit_item.connect("activate", lambda _: Gtk.main_quit())
        self.menu.append(quit_item)

        self.menu.show_all()

    def update_icon(self):
        icon_name = self.get_icon_name()
        if HAS_APP_INDICATOR:
            self.indicator.set_icon_full(icon_name, "Hesland ScreenMatrix")
        else:
            self.status_icon.set_from_icon_name(icon_name)

    def switch_mode(self, mode_name):
        self.config["mode"] = mode_name
        apply_mode(mode_name, self.config)
        self.update_icon()
        self.build_menu()

    def set_position(self, pos):
        self.config["secondary_position"] = pos
        self.config["mac_position"] = pos
        save_config(self.config)
        cur = normalize_mode(self.config.get("mode"))
        if cur in ["linux-only", "linux-win", "terminal-only"]:
            apply_mode(cur, self.config)
        self.build_menu()

    def set_audio(self, audio_policy):
        self.config["mode3_audio"] = audio_policy
        save_config(self.config)
        if normalize_mode(self.config.get("mode")) == "win-only":
            apply_mode("win-only", self.config)
        self.build_menu()

    def set_language(self, lang):
        self.config["lang"] = lang
        save_config(self.config)
        self.build_menu()

    def toggle_win_key(self, widget):
        self.config["capture_win_key"] = widget.get_active()
        save_config(self.config)
        if normalize_mode(self.config.get("mode")) == "win-only":
            apply_mode("win-only", self.config)

    def open_control_panel(self, _):
        import subprocess
        project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        bin_path = os.path.join(project_dir, "bin", "screen-matrix")
        subprocess.Popen([sys.executable, bin_path, "--gui"])

    def on_status_icon_popup(self, icon, button, time):
        self.build_menu()
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, time)

def main():
    tray = ScreenMatrixTray()
    Gtk.main()

if __name__ == "__main__":
    main()
