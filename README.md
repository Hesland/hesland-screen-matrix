# Hesland ScreenMatrix

<p align="center">
  <b>Multi-Modal Display & Input Synergy Hub for Dual-PC (Windows Workstation + Linux Mint)</b><br>
  <i>Seamlessly switch between native dual-screen development, KVM hardware sharing, and ultra-low-latency display streaming.</i>
</p>

<p align="center">
  <a href="#english">English Documentation</a> •
  <a href="#中文说明">中文说明</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux%20Mint%20(Cinnamon%20%7C%20X11)-brightgreen.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Companion-Windows%2010%2F11-blue.svg" alt="Companion OS">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

<a name="english"></a>
## 🌐 English Documentation

### Overview

**Hesland ScreenMatrix** is an open-source display and input synergy system tailored for power developers utilizing a **dual-computer workstation setup**:
- **Primary Workstation**: Windows 10/11 high-performance gaming/compilation rig (equipped with an Ultrawide 3440x1440 240Hz DP display).
- **Secondary Developer Machine**: **Linux Mint (Cinnamon / X11)** (portable or laptop form-factor with high-resolution Retina/2560x1600 internal display).

ScreenMatrix coordinates X11/RandR, Cinnamon desktop layouts, Barrier KVM software, and Sunshine/Moonlight streaming to enable instant one-click switching among three distinct workstation paradigms.

---

### 🌟 The Three Core Workstation Modes

| Mode | Visual Topology & Resolution | Input & Keyboard Routing | Audio & Peripheral Policy | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Mode 1: Linux Mint Native Dual-Screen** | Ultrawide display (MiniDP 3440x1440 60Hz Primary) + Linux Mint Display (2560x1600 Secondary) | Unified Linux Mint keyboard & mouse | Linux Mint local audio | Immersive Linux programming, full-screen IDE, deep debugging |
| **Mode 2: Native Dual-OS KVM** | Ultrawide dedicated to Windows (240Hz DP), Linux Mint display acts as independent Linux terminal | Seamless mouse slide across borders via **Barrier** (custom hotkeys available) | Independent audio per machine | Windows gaming/browsing while monitoring Linux services |
| **Mode 3: Linux Mint as Windows Extended Screen** | Windows outputs to 2 displays: Ultrawide (Display 1 @ 240Hz) + Linux Mint Display (Display 2 @ 2560x1600 via Moonlight stream) | Linux Mint keyboard & mouse directly control Windows session with full **Windows Key passthrough** | **Locked strictly to Windows physical speakers** (Linux Mint 100% muted) | Windows multi-monitor productivity, reference docs & video playback |

---

### 🚀 Key Engineering Highlights

1. **Anti-Rollback Display Sync (Mode 1)**:
   - Precisely calibrated with Cinnamon's internal monitor daemon (`cinnamon-monitors.xml`). Keeps DP-1 as primary at `(0, 0)` and internal display at `(3440, 0)`. Completely prevents desktop environment reset/rollback upon re-plugging MiniDP cables.
2. **Audio Leak & Virtual Sink Lockout Fix (Mode 3)**:
   - Uses `SDL_AUDIODRIVER=dummy` coupled with `--audio-on-host` on the client. **Linux Mint speakers remain 100% silent**, while Windows physical speakers/soundbars output native uncompressed audio without being hijacked by virtual drivers.
3. **Full Windows Key & Shortcut Passthrough (Mode 3)**:
   - Enforces `--capture-system-keys always`, allowing `Win`, `Win+D`, `Win+E`, `Win+Tab`, and `Alt+Tab` to seamlessly control Windows workspace windows without getting intercepted by the host desktop.
4. **Dynamic Physical Screen Placement**:
   - Easily toggle whether the Linux Mint display sits to the **LEFT** or **RIGHT** of your main Ultrawide display. Barrier links and X11 coordinates adjust on the fly without restarting your session.
5. **System Tray Applet & Graphical Control Panel**:
   - Native GTK3 system tray icon (with right-click quick menu) and a modern visual control panel. Supports both English and Chinese locales.

---

### 📦 Installation (Linux Mint)

```bash
# Clone the repository
git clone https://github.com/Hesland/hesland-screen-matrix.git
cd hesland-screen-matrix

# Run one-click installer
chmod +x install.sh
./install.sh
```

The installer will:
1. Deploy binaries to `~/.local/bin/screen-matrix`.
2. Register a user-level systemd service (`screen-matrix-tray.service`) for the system tray applet.
3. Bind existing shortcuts (`Ctrl+Alt+M` for rotation, `Super+F12` for toggle) directly to ScreenMatrix.
4. Add a desktop entry in the application menu.

---

### 🛠️ CLI Reference

```bash
# Switch Modes
screen-matrix 1                  # Enter Mode 1 (Linux Mint Native Dual-Screen)
screen-matrix 2                  # Enter Mode 2 (Dual-OS KVM)
screen-matrix 3                  # Enter Mode 3 (Windows Extended Display)
screen-matrix cycle              # Cycle modes: 1 -> 2 -> 3 -> 1 (Ctrl+Alt+M)
screen-matrix toggle             # Toggle Mode 1 and Mode 2 (Super+F12)

# Change Placement
screen-matrix --pos right        # Linux Mint display on the RIGHT of Ultrawide
screen-matrix --pos left         # Linux Mint display on the LEFT of Ultrawide
screen-matrix --pos toggle       # Flip placement instantly

# Audio Strategy (Mode 3)
screen-matrix --audio windows    # Lock audio to Windows physical speakers (Recommended)
screen-matrix --audio both       # Simultaneous dual-device audio
screen-matrix --audio mac        # Linux Mint local speaker only

# GUI & Status
screen-matrix --gui              # Open graphical GTK control panel
screen-matrix --tray             # Launch background tray applet
screen-matrix --status           # Print configuration JSON
screen-matrix --lang en          # Set UI language to English (default)
screen-matrix --lang zh          # Set UI language to Chinese
```

---

### ⚙️ Configuration File

Settings are automatically persisted at `~/.config/screen-matrix/config.json`:
```json
{
    "lang": "en",
    "mode": 1,
    "secondary_position": "right",
    "mode3_audio": "windows_only",
    "capture_win_key": true,
    "windows_ip": "192.168.1.100",
    "ultrawide_res": "3440x1440",
    "ultrawide_rate": "60",
    "secondary_res": "2560x1600",
    "secondary_rate": "59.97"
}
```

---

<br>
<hr>
<br>

<a name="中文说明"></a>
## 🇨🇳 中文说明

### 系统概述

**Hesland ScreenMatrix** 是一套专为 **双机双系统（Windows 主力工作站 + Linux Mint 开发副机）** 打造的跨屏与键鼠协同调度中枢：
- **主力工作站**：Windows 10/11 高性能游戏/编译机（连接 3440x1440 240Hz DP 带鱼屏）。
- **开发副机**：**Linux Mint (Cinnamon / X11)** 操作系统（笔记本或便携主机，具备 2560x1600 高清内建屏幕）。

ScreenMatrix 深度整合 X11/RandR 底层坐标映射、Linux Mint (Cinnamon) 监视器配置、Barrier 局域网无缝键鼠穿透与 Sunshine/Moonlight 极速低延迟串流，实现单键或系统托盘在三大工作形态之间瞬间流转。

---

### 🌟 三大核心工作形态

| 工作形态 | 画面与分辨率拓扑 | 键鼠与输入行为 | 音频路由策略 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **形态 1：Linux Mint 双屏沉浸开发** | 带鱼屏（MiniDP 3440x1440 60Hz 主屏）+ Linux Mint 本地屏幕（2560x1600 副屏） | Linux 键鼠全局控制双屏 | Linux Mint 本地音频 | 沉浸式 Linux 编码、全屏 IDE 调试 |
| **形态 2：原生双系统 KVM 穿透** | 带鱼屏归 Windows（DP 240Hz 电竞主力），Linux Mint 屏幕为独立控制台 | **Barrier** 局域网无缝键鼠穿透，滑过屏幕边缘即切机 | 各自独立系统发声 | 主机打游戏 / 查资料，副机监控编译 |
| **形态 3：Linux Mint 作为 Windows 副屏扩展** | 带鱼屏为 Windows 1 屏（240Hz），Linux Mint 本地屏幕作为 Windows 2 屏扩展（Moonlight 串流） | Linux Mint 键鼠直接操作 Windows 扩展屏（支持 Win 键与组合键完整穿透） | **锁定仅 Windows 物理音响发声**（Linux Mint 本地 100% 绝对静音） | Windows 多任务办公、代码查阅与视频播放 |

---

### 🚀 攻克的核心技术难点

1. **彻底解决形态 1 屏幕回滚与错位**：
   - 严格匹配 Linux Mint (Cinnamon) 原生监视器守护规则，将 DP-1 锚定为 `(0, 0)` 主屏、内建屏置于 `(3440, 0)`，MiniDP 热插拔再也不会发生坐标漂移与回滚重置。
2. **彻底解决形态 3 双响与虚拟声卡劫持**：
   - 客户端通过 `SDL_AUDIODRIVER=dummy` 结合 `--audio-on-host`，**Linux Mint 本地扬声器 100% 绝对物理静音**，Windows 物理音箱/带鱼屏音响独占原声播放，不再被虚拟声卡绑架。
3. **彻底解决形态 3 Win 键失效**：
   - 强制启用 `--capture-system-keys always`，Win 键、`Win+D`、`Win+Tab` 组合键完整穿透给 Windows 桌面，跨窗切换随心所欲。
4. **屏幕相对物理拓扑动态参数化**：
   - 随时一键修改 Linux Mint 屏幕位于带鱼屏的【左侧】还是【右侧】，Barrier 穿透方向与 X11 布局无缝即时生效。
5. **系统状态栏托盘 Applet 与图形控制面板**：
   - Linux Mint 任务栏原生托盘，右键秒切模式；自带 GTK3 控制面板，支持中英双语自适应切换。

---

### 📦 安装部署 (Linux Mint)

```bash
# 克隆仓库
git clone https://github.com/Hesland/hesland-screen-matrix.git
cd hesland-screen-matrix

# 执行一键安装
chmod +x install.sh
./install.sh
```

### 快捷键定义
- `Ctrl + Alt + M`：三模自动轮转（1 -> 2 -> 3 -> 1）
- `Super + F12`：形态 1 与形态 2 快速互切
- `Ctrl + Alt + S`：Barrier 焦点强制切入 Windows
- `Ctrl + Alt + A`：Barrier 焦点强制切回 Linux Mint

---

## ⚖️ License

MIT License. Copyright (c) 2026 Hesland.
