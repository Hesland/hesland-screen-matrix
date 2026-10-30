import os
import locale

TRANSLATIONS = {
    "en": {
        "app_title": "Hesland ScreenMatrix Control Panel",
        "app_subtitle": "Cross-System Screen Switching · Dual-PC Topology · Audio & Keyboard Routing",
        "core_modes": "Core Operation Modes",
        "mode1_label": "Mode 1: Linux Mint Dual-Screen (Ultrawide 3440x1440 60Hz + Linux Display)",
        "mode2_label": "Mode 2: Native Dual-OS KVM (Windows 240Hz DP + Linux Mint Barrier)",
        "mode3_label": "Mode 3: Linux Mint as Windows Secondary Display (Moonlight Stream)",
        "topology_label": "📐 Screen Physical Placement (Linux Mint relative to Ultrawide)",
        "pos_right_label": "Linux Mint on 【RIGHT】 (Ultrawide on Left: slide left into Windows)",
        "pos_left_label": "Linux Mint on 【LEFT】 (Ultrawide on Right: slide right into Windows)",
        "mode3_adv": "⚙️ Mode 3 (Secondary Display) Advanced Control",
        "audio_label": "🔊 Audio Routing Strategy:",
        "audio_win": "Lock to Windows physical speakers only (Linux Mint muted)",
        "audio_both": "Dual-device simultaneous playback (Windows + Linux Mint)",
        "audio_mint": "Linux Mint local speaker only",
        "win_key_label": "⌨️ Pass through Windows/Super key directly to Windows session",
        "btn_close": "Close",
        "btn_save": "💾 Save & Apply Now",
        "lang_label": "🌐 Language / 语言:",
        # Tray items
        "tray_m1": "🖥️ Mode 1: Linux Mint Dual Display (3440x1440)",
        "tray_m2": "⚡ Mode 2: Native Dual-OS KVM (Barrier)",
        "tray_m3": "🪟 Mode 3: Linux Mint as Windows Extended Screen",
        "tray_pos_menu": "📐 Linux Mint Display Position",
        "tray_pos_right": "Placed on Right (Ultrawide on Left)",
        "tray_pos_left": "Placed on Left (Ultrawide on Right)",
        "tray_audio_menu": "🔊 Mode 3 Audio Output Strategy",
        "tray_audio_win": "Lock to Windows Speakers (Linux Muted)",
        "tray_audio_both": "Simultaneous Dual-Device Audio",
        "tray_audio_mint": "Linux Mint Local Speakers Only",
        "tray_win_key": "⌨️ Forward Win Key to Windows (Mode 3)",
        "tray_gui": "⚙️ Open Control Panel (GUI)...",
        "tray_quit": "🚪 Quit Tray",
        # Notifications
        "notif_m1_title": "🖥️ [Mode 1] Linux Mint Dual Screen",
        "notif_m1_msg": "Ultrawide 3440x1440 60Hz active on Linux Mint!\nLayout locked, no rollback.",
        "notif_m2_title": "⚡ [Mode 2] Native Dual-OS KVM",
        "notif_m2_msg": "Ultrawide dedicated to Windows 240Hz! Linux Mint on 【{pos}】.\n{tip}\n(Press Ctrl+Alt+S for Windows, Ctrl+Alt+A for Linux)",
        "notif_m3_title": "🖥️ [Mode 3] Linux Mint as Extended Screen",
        "notif_m3_msg": "Ultrawide is Windows Primary, Linux Mint is Extended Display!\n{audio_tip}\n{key_tip}",
        "notif_pos_title": "⚡ [Barrier Topology Updated]",
        "notif_pos_msg": "Linux Mint display set to 【{pos}】!\n{tip}\n(Press Ctrl+Alt+S / A to switch)",
        "slide_tip_right": "Slide mouse LEFT into Windows, Windows mouse RIGHT into Linux",
        "slide_tip_left": "Slide mouse RIGHT into Windows, Windows mouse LEFT into Linux",
        "audio_tip_win": "🔊 Audio locked to Windows physical speakers only (Linux muted)",
        "audio_tip_both": "🔊 Audio outputting from both Windows & Linux speakers",
        "audio_tip_mint": "🔊 Audio outputting only from Linux local speakers",
        "key_tip_on": "⌨️ Win key forwarded to Windows session",
        "key_tip_off": "⌨️ Win key kept on Linux Mint local desktop"
    },
    "zh": {
        "app_title": "Hesland ScreenMatrix 控制面板",
        "app_subtitle": "跨系统屏幕模式切换 · 双机物理拓扑管理 · 音频与按键调度中枢 (专为 Linux Mint 打造)",
        "core_modes": "核心工作形态选择",
        "mode1_label": "形态 1: Linux Mint 双屏沉浸开发 (带鱼屏 3440x1440 60Hz + 本地屏幕)",
        "mode2_label": "形态 2: 原生双系统穿透 (带鱼屏归 Windows 240Hz, Barrier 键鼠穿透)",
        "mode3_label": "形态 3: Linux Mint 作为 Windows 副屏扩展 (Sunshine + Moonlight 串流)",
        "topology_label": "📐 屏幕物理摆放 (Linux Mint 相对带鱼屏位置)",
        "pos_right_label": "Linux Mint 在【右侧】 (带鱼屏在左，Linux 在右：鼠标往左滑入 Win)",
        "pos_left_label": "Linux Mint 在【左侧】 (带鱼屏在右，Linux 在左：鼠标往右滑入 Win)",
        "mode3_adv": "⚙️ 模式 3 (串流副屏) 高级控制",
        "audio_label": "🔊 声音输出策略:",
        "audio_win": "锁定仅 Windows 物理音响 (推荐：Linux 本机 100% 绝对静音)",
        "audio_both": "双端同时发声 (Windows 音响 + Linux 本地扬声器)",
        "audio_mint": "仅 Linux Mint 本地扬声器发声",
        "win_key_label": "⌨️ 捕获并穿透 Win 键 (在副屏上按 Win 键直接响应 Windows)",
        "btn_close": "关闭",
        "btn_save": "💾 保存并立即生效",
        "lang_label": "🌐 Language / 语言:",
        # 托盘菜单
        "tray_m1": "🖥️ 模式 1: Linux Mint 本地双屏 (3440x1440)",
        "tray_m2": "⚡ 模式 2: 原生双系统穿透 (Barrier 键鼠)",
        "tray_m3": "🪟 模式 3: Linux Mint 作为 Windows 副屏扩展",
        "tray_pos_menu": "📐 Linux Mint 屏幕相对位置",
        "tray_pos_right": "放在右侧 (带鱼屏在左，Linux 在右)",
        "tray_pos_left": "放在左侧 (带鱼屏在右，Linux 在左)",
        "tray_audio_menu": "🔊 模式 3 声音输出策略",
        "tray_audio_win": "锁定仅 Windows 物理音响 (Linux 静音)",
        "tray_audio_both": "两台设备同时播放 (双端发声)",
        "tray_audio_mint": "仅 Linux Mint 本地扬声器发声",
        "tray_win_key": "⌨️ 模式 3 穿透 Win 键给 Windows",
        "tray_gui": "⚙️ 打开控制面板 (GUI)...",
        "tray_quit": "🚪 退出托盘",
        # 通知提示
        "notif_m1_title": "🖥️ [形态 1] Linux Mint 双屏模式",
        "notif_m1_msg": "带鱼屏原生 3440x1440 60Hz 归 Linux Mint 主屏！\n副屏已对齐，配置锁定不回滚。",
        "notif_m2_title": "⚡ [形态 2] 原生双系统穿透",
        "notif_m2_msg": "带鱼屏归 Windows 240Hz！Linux Mint 在【{pos}】。\n{tip}\n(按 Ctrl+Alt+S 进入 Windows，Ctrl+Alt+A 切回 Linux)",
        "notif_m3_title": "🖥️ [形态 3] Linux Mint 作为副屏扩展",
        "notif_m3_msg": "带鱼屏为 Windows 主屏，Linux Mint 为副屏！\n{audio_tip}\n{key_tip}",
        "notif_pos_title": "⚡ [Barrier 屏幕拓扑更新]",
        "notif_pos_msg": "Linux Mint 屏幕已设为【{pos}】！\n{tip}\n(按 Ctrl+Alt+S / A 可强制切屏)",
        "slide_tip_right": "Linux 鼠标往【左】滑进入 Windows，Windows 鼠标往【右】滑进入 Linux",
        "slide_tip_left": "Linux 鼠标往【右】滑进入 Windows，Windows 鼠标往【左】滑进入 Linux",
        "audio_tip_win": "🔊 声音已锁定仅在 Windows 音箱输出 (Linux Mint 完全静音)",
        "audio_tip_both": "🔊 声音由 Windows 音箱与 Linux 扬声器同时输出",
        "audio_tip_mint": "🔊 声音仅由 Linux 本地扬声器输出",
        "key_tip_on": "⌨️ Win 键已穿透至 Windows 会话 (可用 Win 组合键)",
        "key_tip_off": "⌨️ Win 键保留在 Linux Mint 本地"
    }
}

def get_current_lang(cfg=None):
    if cfg and "lang" in cfg:
        l = cfg["lang"].lower()
        if l in ["zh", "cn", "zh_cn", "zh-cn", "chinese"]:
            return "zh"
        if l in ["en", "en_us", "en-us", "english"]:
            return "en"
    # Default to English as requested
    return "en"

def t(key, cfg=None, **kwargs):
    lang = get_current_lang(cfg)
    msg = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return msg.format(**kwargs)
        except Exception:
            return msg
    return msg
