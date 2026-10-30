# Hesland ScreenMatrix

<p align="center">
  <b>Multi-Modal Display & Input Synergy Hub for Dual-PC (Windows Workstation + Linux Mint)</b><br>
  <i>Seamlessly switch between native dual-screen development, KVM hardware sharing, Windows display streaming, and pure terminal companion modes.</i>
</p>

<p align="center">
  <a href="#english">English Documentation</a> •
  <a href="#中文说明">中文说明</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux%20Mint%20(Cinnamon%20%7C%20X11)-brightgreen.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Companion-Windows%2010%2F11-blue.svg" alt="Companion OS">
  <img src="https://img.shields.io/badge/Modes-4%20Workstation%20Paradigms-purple.svg" alt="Modes">
  <img src="https://img.shields.io/badge/Edition-Full%20GUI%20%7C%20Terminal--Only-orange.svg" alt="Editions">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

<a name="english"></a>
## 🌐 English Documentation

### Overview

**Hesland ScreenMatrix** is an open-source display and input synergy system tailored for power developers utilizing a **dual-computer workstation setup**:
- **Primary Workstation**: Windows 10/11 high-performance gaming/compilation rig (equipped with an Ultrawide 3440x1440 240Hz DP display).
- **Secondary Developer Machine**: **Linux Mint (Cinnamon / X11)** (portable or laptop form-factor with high-resolution Retina/2560x1600 internal display).

ScreenMatrix coordinates X11/RandR, Cinnamon desktop layouts, Barrier KVM software, and Sunshine/Moonlight streaming to enable instant one-click switching among four distinct workstation paradigms.

---

### 🌟 The Four Workstation Operation Modes

| Command | Visual Topology & Resolution | Input & Keyboard Routing | Audio & Clipboard Policy | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **`screen-matrix linux-only`** | Ultrawide display (MiniDP 3440x1440 60Hz Primary) + Linux Mint Display (2560x1600 Secondary) | Unified Linux Mint keyboard & mouse | Linux Mint local audio | Immersive Linux programming, full-screen IDE, deep local debugging |
| **`screen-matrix linux-win`** | Ultrawide dedicated to Windows (240Hz DP), Linux Mint display acts as independent Linux desktop | Seamless mouse slide across borders via **Barrier** | Independent audio per machine; **bi-directional clipboard sharing** | Windows gaming/browsing while monitoring Linux services |
| **`screen-matrix win-only`** | Windows outputs to 2 displays: Ultrawide (Display 1 @ 240Hz) + Linux Mint Display (Display 2 @ 2560x1600 via Moonlight stream) | Linux Mint keyboard & mouse directly control Windows session with full **Windows Key passthrough** | **Locked strictly to Windows physical speakers** (Linux Mint 100% muted) | Windows multi-monitor productivity, reference docs & video playback |
| **`screen-matrix terminal-only`** ⭐ | Ultrawide dedicated to Windows (240Hz DP), Linux Mint display runs an **unobstructed fullscreen CLI terminal** | Switch keyboard/mouse focus seamlessly via **`Ctrl+Alt+Space`** or **`Ctrl+Alt+S/A`** | **Bi-directional shared clipboard** (`Ctrl+C` in Windows, `Ctrl+Shift+V` in Linux Terminal) | Exploring Linux command-line on a dedicated machine without WSL or VM bloat |

---

### 💡 Highlight: `terminal-only` Mode

For Windows power users who want a physical Linux machine side-by-side to learn or work with pure Linux CLI — without setting up WSL, virtual machines, or relying on SSH window tools like FinalShell:
- **Zero Distraction Visuals**: The Linux Mint display automatically launches or focuses a distraction-free fullscreen terminal session.
- **Instant KVM Toggle**: Press **`Ctrl+Alt+Space`** (or `Ctrl+Alt+S` for Windows, `Ctrl+Alt+A` for Linux) to swap keyboard and mouse control immediately between your Windows desktop and the Linux terminal.
- **Bi-Directional Shared Clipboard**: Copy commands, code snippets, or error logs in Windows with `Ctrl+C` and paste them directly into your Linux terminal with `Ctrl+Shift+V`, and vice-versa.

---

### 💻 Terminal-Only Edition (Zero GUI Dependencies)

For headless servers, minimal window managers (i3, bspwm, sway, tmux), or command-line power users, ScreenMatrix provides a **Terminal-Only Edition** that requires **0 GTK / PyGObject dependencies**:

#### 1. Quick Install (Terminal Only)
```bash
git clone https://github.com/Hesland/hesland-screen-matrix.git
cd hesland-screen-matrix
chmod +x install-terminal-only.sh
./install-terminal-only.sh
```

#### 2. Interactive Terminal Dashboard (TUI)
Simply run `screen-matrix` without flags (or `screen-matrix --tui`) to launch a colorized ASCII control panel directly inside your terminal:
```text
╔════════════════════════════════════════════════════════════════════════════╗
║              🖥️  Hesland ScreenMatrix (Terminal-Only TUI)                  ║
║      Cross-System Dual-PC Display Synergy Hub for Linux Mint + Windows     ║
╠════════════════════════════════════════════════════════════════════════════╣
║  [1] linux-only   : Linux Mint Native Dual-Screen (3440x1440)      [ACTIVE]║
║  [2] linux-win    : Native Dual-OS KVM (Windows 240Hz + Barrier)           ║
║  [3] win-only     : Windows Extended Display (Stream to Mint)              ║
║  [4] terminal-only: Pure Linux Terminal Companion (Shared Clip)            ║
╠════════════════════════════════════════════════════════════════════════════╣
║  Placement    :  [R] Right (*)   /   [L] Left                              ║
║  win-only Aud :  [W] Windows Only (*) | [B] Both | [M] Linux Mint          ║
║  Win Key Fwd  :  [K] Enabled (Always)                                      ║
║  Language     :  [G] EN (Toggle English / 中文)                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║  Actions: [C] Cycle Modes  |  [T] Toggle 1&2  |  [S] Status  |  [Q] Quit   ║
╚════════════════════════════════════════════════════════════════════════════╝
```
Type `1`, `2`, `3`, `4`, `r`, `l`, `w`, or `k` to change settings on the fly.

#### 3. Windows-Side Terminal CLI Companion
Run commands directly from Windows PowerShell / Terminal to trigger Linux Mint display modes remotely:
```powershell
cd windows
.\screen-matrix.ps1 linux-only         # Tell Linux Mint to switch to linux-only
.\screen-matrix.ps1 linux-win          # Switch to linux-win (Barrier)
.\screen-matrix.ps1 win-only           # Switch to win-only (Moonlight stream)
.\screen-matrix.ps1 terminal-only      # Switch to terminal-only companion
.\screen-matrix.ps1 -Pos right         # Change display placement
.\screen-matrix.ps1 -Status            # Query Linux Mint configuration JSON
```

---

### 📦 Full Installation (With System Tray & GTK GUI)

```bash
# Clone the repository
git clone https://github.com/Hesland/hesland-screen-matrix.git
cd hesland-screen-matrix

# Run one-click installer
chmod +x install.sh
./install.sh
```

---

### 🛠️ CLI Reference

```bash
# Switch Modes
screen-matrix linux-only         # Enter Mode 1 (Linux Mint Native Dual-Screen)
screen-matrix linux-win          # Enter Mode 2 (Dual-OS KVM)
screen-matrix win-only           # Enter Mode 3 (Windows Extended Display)
screen-matrix terminal-only      # Enter Mode 4 (Pure Terminal Companion)
screen-matrix cycle              # Cycle modes: 1 -> 2 -> 3 -> 4 (Ctrl+Alt+M)
screen-matrix toggle             # Toggle between linux-only and linux-win (Super+F12)

# Change Placement
screen-matrix --pos right        # Linux Mint display on the RIGHT of Ultrawide
screen-matrix --pos left         # Linux Mint display on the LEFT of Ultrawide
screen-matrix --pos toggle       # Flip placement instantly

# Audio Strategy (win-only)
screen-matrix --audio windows    # Lock audio to Windows physical speakers (Recommended)
screen-matrix --audio both       # Simultaneous dual-device audio
screen-matrix --audio mac        # Linux Mint local speaker only

# Terminal Dashboard & GUI
screen-matrix                    # Launch interactive terminal TUI dashboard
screen-matrix --gui              # Open graphical GTK control panel
screen-matrix --tray             # Launch background tray applet
screen-matrix --status           # Print configuration JSON
screen-matrix --lang en          # Set UI language to English (default)
screen-matrix --lang zh          # Set UI language to Chinese
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

ScreenMatrix 深度整合 X11/RandR 底层坐标映射、Linux Mint (Cinnamon) 监视器配置、Barrier 局域网无缝键鼠穿透与 Sunshine/Moonlight 极速低延迟串流，实现单键或系统托盘在四大工作形态之间瞬间流转。

---

### 🌟 四大核心工作形态

| 触发命令 | 画面与分辨率分配 | 键鼠与输入行为 | 音频与剪贴板策略 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **`screen-matrix linux-only`** | 带鱼屏（MiniDP 3440x1440 60Hz 主屏）+ Linux Mint 本地屏幕（2560x1600 副屏） | Linux 键鼠全局控制双屏 | Linux Mint 本地音频 | 沉浸式 Linux 编码、全屏 IDE 调试 |
| **`screen-matrix linux-win`** | 带鱼屏归 Windows（DP 240Hz 电竞主力），Linux Mint 屏幕为独立桌面控制台 | **Barrier** 局域网无缝键鼠穿透，滑过屏幕边缘即切机 | 各自独立系统发声；**支持双向剪贴板共享** | 主机打游戏 / 查资料，副机监控编译 |
| **`screen-matrix win-only`** | 带鱼屏为 Windows 1 屏（240Hz），Linux Mint 本地屏幕作为 Windows 2 屏扩展（Moonlight 串流） | Linux Mint 键鼠直接操作 Windows 扩展屏（支持 Win 键与组合键完整穿透） | **锁定仅 Windows 物理音响发声**（Linux Mint 本地 100% 绝对静音） | Windows 多任务办公、代码查阅与视频播放 |
| **`screen-matrix terminal-only`** ⭐ | 带鱼屏归 Windows（DP 240Hz），Linux Mint 屏幕化身为**纯净全屏沉浸终端机** | 按快捷键 **`Ctrl+Alt+Space`** 或 **`Ctrl+Alt+S/A`** 瞬间交替主控 | **双向共享剪贴板**（Win 复制 `Ctrl+C`，Linux 终端直接粘贴 `Ctrl+Shift+V`） | Windows 用户免 WSL/免虚拟机无缝联动物理 Linux 终端 |

---

### 💡 核心创新：`terminal-only` 模式详解

对于主要在 Windows 上工作，没有安装 WSL 或不想开沉重虚拟机，又希望通过双机联动熟悉并使用纯正 Linux 命令行的新手极客：
- **纯粹无干扰**：副屏自动全屏唤起无杂项干扰的纯终端会话。
- **单键主控交替**：按 **`Ctrl+Alt+Space`**（或 `Ctrl+Alt+S` 切 Windows，`Ctrl+Alt+A` 切 Linux），一套键鼠在 Windows 工作区与 Linux 终端之间随心互换！
- **双向剪贴板秒通**：在 Windows 查阅教程、拷贝 Shell 命令，切过去即可直接贴入 Linux 终端执行；Linux 终端输出的报错或日志，复制后切回 Windows 即可随处粘贴！

---

### 💻 纯终端精简版 (Terminal-Only Edition，零 GUI 依赖)

面向无头开发机（Headless Server）、平铺窗口管理器（i3, bspwm, sway, tmux）或喜欢纯终端工作的极客，ScreenMatrix 提供了**零 GUI / 零 GTK 依赖的纯终端精简版**：

#### 1. 终端精简版一键安装
```bash
git clone https://github.com/Hesland/hesland-screen-matrix.git
cd hesland-screen-matrix
chmod +x install-terminal-only.sh
./install-terminal-only.sh
```

#### 2. 彩色交互式终端控制面板 (TUI Dashboard)
在终端直接输入 `screen-matrix`（或 `screen-matrix --tui`），即可拉起高质感 ASCII 彩色控制面板：
- 键盘敲 `1` / `2` / `3` / `4`：秒切对应四大形态；
- 敲 `r` / `l`：即时切换屏幕左右相对摆放位置；
- 敲 `w` / `b` / `m`：即时切换声音输出策略；
- 敲 `k`：开关 Win 键穿透；
- 敲 `g`：秒切中英双语；
- 敲 `q`：退出交互。

#### 3. Windows 端纯命令行协同控制
在 Windows PowerShell 或 Windows Terminal 中直接敲命令，远程调度 Linux Mint 屏幕状态：
```powershell
cd windows
.\screen-matrix.ps1 linux-only         # 远程通知 Linux Mint 切换形态 1
.\screen-matrix.ps1 linux-win          # 远程切换形态 2 (Barrier)
.\screen-matrix.ps1 win-only           # 远程切换形态 3 (Moonlight)
.\screen-matrix.ps1 terminal-only      # 远程切换形态 4 (纯终端伴侣)
.\screen-matrix.ps1 -Pos right         # 远程调整副屏左右位置
.\screen-matrix.ps1 -Status            # 查询当前配置状态
```

---

## ⚖️ License

MIT License. Copyright (c) 2026 Hesland.
