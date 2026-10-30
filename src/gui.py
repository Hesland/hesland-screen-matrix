import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .config import load_config, save_config, normalize_mode
from .core import apply_mode
from .i18n import t

class ControlPanelWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.set_title(t("app_title", self.config))
        self.set_border_width(18)
        self.set_default_size(560, 680)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(self.main_box)
        self.render_ui()

    def render_ui(self):
        for child in self.main_box.get_children():
            self.main_box.remove(child)

        cfg = self.config

        # 1. Header with Language Switcher
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        title_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>🖥️ {t('app_title', cfg)}</span>")
        title_label.set_xalign(0)
        title_vbox.pack_start(title_label, False, False, 0)

        sub_label = Gtk.Label()
        sub_label.set_markup(f"<span size='small' color='#666'>{t('app_subtitle', cfg)}</span>")
        sub_label.set_xalign(0)
        title_vbox.pack_start(sub_label, False, False, 0)
        header_box.pack_start(title_vbox, True, True, 0)

        # Language dropdown
        lang_combo = Gtk.ComboBoxText()
        lang_combo.append("en", "English")
        lang_combo.append("zh", "中文")
        lang_combo.set_active(0 if cfg.get("lang", "en") == "en" else 1)
        lang_combo.connect("changed", self.on_lang_changed)
        header_box.pack_end(lang_combo, False, False, 0)

        self.main_box.pack_start(header_box, False, False, 0)
        self.main_box.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        # 2. 4 Mode Cards
        mode_frame = Gtk.Frame(label=t("core_modes", cfg))
        mode_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        mode_box.set_border_width(12)
        mode_frame.add(mode_box)
        self.main_box.pack_start(mode_frame, False, False, 0)

        self.mode_btn1 = Gtk.RadioButton.new_with_label(None, t("mode_linux_only", cfg))
        self.mode_btn2 = Gtk.RadioButton.new_with_label_from_widget(self.mode_btn1, t("mode_linux_win", cfg))
        self.mode_btn3 = Gtk.RadioButton.new_with_label_from_widget(self.mode_btn1, t("mode_win_only", cfg))
        self.mode_btn4 = Gtk.RadioButton.new_with_label_from_widget(self.mode_btn1, t("mode_terminal_only", cfg))

        cur_mode = normalize_mode(cfg.get("mode"))
        if cur_mode == "linux-only":
            self.mode_btn1.set_active(True)
        elif cur_mode == "linux-win":
            self.mode_btn2.set_active(True)
        elif cur_mode == "win-only":
            self.mode_btn3.set_active(True)
        else:
            self.mode_btn4.set_active(True)

        mode_box.pack_start(self.mode_btn1, False, False, 0)
        mode_box.pack_start(self.mode_btn2, False, False, 0)
        mode_box.pack_start(self.mode_btn3, False, False, 0)
        mode_box.pack_start(self.mode_btn4, False, False, 0)

        # 3. Placement
        pos_frame = Gtk.Frame(label=t("topology_label", cfg))
        pos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        pos_box.set_border_width(12)
        pos_frame.add(pos_box)
        self.main_box.pack_start(pos_frame, False, False, 0)

        self.pos_right = Gtk.RadioButton.new_with_label(None, t("pos_right_label", cfg))
        self.pos_left = Gtk.RadioButton.new_with_label_from_widget(self.pos_right, t("pos_left_label", cfg))

        cur_pos = cfg.get("secondary_position", cfg.get("mac_position", "right"))
        if cur_pos == "right":
            self.pos_right.set_active(True)
        else:
            self.pos_left.set_active(True)

        pos_box.pack_start(self.pos_right, False, False, 0)
        pos_box.pack_start(self.pos_left, False, False, 0)

        # 4. win-only Advanced Options
        m3_frame = Gtk.Frame(label=t("mode3_adv", cfg))
        m3_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        m3_box.set_border_width(12)
        m3_frame.add(m3_box)
        self.main_box.pack_start(m3_frame, False, False, 0)

        audio_label = Gtk.Label()
        audio_label.set_markup(f"<b>{t('audio_label', cfg)}</b>")
        audio_label.set_xalign(0)
        m3_box.pack_start(audio_label, False, False, 0)

        self.audio_win = Gtk.RadioButton.new_with_label(None, t("audio_win", cfg))
        self.audio_both = Gtk.RadioButton.new_with_label_from_widget(self.audio_win, t("audio_both", cfg))
        self.audio_mint = Gtk.RadioButton.new_with_label_from_widget(self.audio_win, t("audio_mint", cfg))

        cur_audio = cfg.get("mode3_audio", "windows_only")
        if cur_audio == "windows_only":
            self.audio_win.set_active(True)
        elif cur_audio == "both":
            self.audio_both.set_active(True)
        else:
            self.audio_mint.set_active(True)

        m3_box.pack_start(self.audio_win, False, False, 0)
        m3_box.pack_start(self.audio_both, False, False, 0)
        m3_box.pack_start(self.audio_mint, False, False, 0)

        self.win_key_check = Gtk.CheckButton.new_with_label(t("win_key_label", cfg))
        self.win_key_check.set_active(cfg.get("capture_win_key", True))
        m3_box.pack_start(self.win_key_check, False, False, 0)

        # 5. Bottom Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        self.main_box.pack_end(btn_box, False, False, 0)

        close_btn = Gtk.Button.new_with_label(t("btn_close", cfg))
        close_btn.connect("clicked", lambda _: self.destroy())
        btn_box.pack_start(close_btn, False, False, 0)

        apply_btn = Gtk.Button.new_with_label(t("btn_save", cfg))
        apply_btn.get_style_context().add_class("suggested-action")
        apply_btn.connect("clicked", self.on_apply_clicked)
        btn_box.pack_start(apply_btn, False, False, 0)

        self.show_all()

    def on_lang_changed(self, combo):
        selected = combo.get_active_id()
        if selected and selected != self.config.get("lang"):
            self.config["lang"] = selected
            save_config(self.config)
            self.set_title(t("app_title", self.config))
            self.render_ui()

    def on_apply_clicked(self, _):
        if self.mode_btn1.get_active():
            new_mode = "linux-only"
        elif self.mode_btn2.get_active():
            new_mode = "linux-win"
        elif self.mode_btn3.get_active():
            new_mode = "win-only"
        else:
            new_mode = "terminal-only"

        new_pos = "right" if self.pos_right.get_active() else "left"

        if self.audio_win.get_active():
            new_audio = "windows_only"
        elif self.audio_both.get_active():
            new_audio = "both"
        else:
            new_audio = "mac_only"

        new_win_key = self.win_key_check.get_active()

        self.config["mode"] = new_mode
        self.config["secondary_position"] = new_pos
        self.config["mac_position"] = new_pos
        self.config["mode3_audio"] = new_audio
        self.config["capture_win_key"] = new_win_key
        save_config(self.config)

        apply_mode(new_mode, self.config)

def main():
    win = ControlPanelWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
