#!/bin/bash
# ==============================================================================
# Hesland ScreenMatrix 安装脚本
# ==============================================================================

set -e

INSTALL_DIR="$HOME/.local/share/screen-matrix"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "🚀 开始部署 ScreenMatrix 屏幕协同中枢..."

# 1. 创建目标目录
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR" "$AUTOSTART_DIR" "$HOME/.config/screen-matrix"

# 2. 复制源码
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/bin" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/data" "$INSTALL_DIR/"

# 3. 赋予可执行权限并链接到 ~/.local/bin
chmod +x "$INSTALL_DIR/bin/screen-matrix"
ln -sf "$INSTALL_DIR/bin/screen-matrix" "$BIN_DIR/screen-matrix"

# 4. 替换旧快捷键脚本 (平滑接管 ~/.screenlayout/mode_switch.sh)
mkdir -p "$HOME/.screenlayout"
cat << 'EOF' > "$HOME/.screenlayout/mode_switch.sh"
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
if [ -n "$1" ]; then
    screen-matrix "$1" "$2"
else
    screen-matrix cycle
fi
EOF
chmod +x "$HOME/.screenlayout/mode_switch.sh"

cat << 'EOF' > "$HOME/.screenlayout/toggle_mode.sh"
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
screen-matrix toggle
EOF
chmod +x "$HOME/.screenlayout/toggle_mode.sh"

# 5. 安装 Desktop 与 Autostart
cp "$INSTALL_DIR/data/screen-matrix.desktop" "$DESKTOP_DIR/"
cp "$INSTALL_DIR/data/autostart.desktop" "$AUTOSTART_DIR/"

# 6. 启动托盘后台服务
pkill -f "screen-matrix --tray" || true
nohup "$BIN_DIR/screen-matrix" --tray >/dev/null 2>&1 &

echo "✅ ScreenMatrix 安装完成！"
echo "👉 系统状态栏托盘已启动"
echo "👉 快捷键 Ctrl+Alt+M (轮转) 与 Super+F12 已无缝托管至 ScreenMatrix"
echo "👉 在终端输入 screen-matrix --gui 可直接打开控制面板"
