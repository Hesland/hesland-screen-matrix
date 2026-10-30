#!/bin/bash
# ==============================================================================
# Hesland ScreenMatrix Terminal-Only Edition Installer
# Zero GUI dependencies, pure CLI & TUI workflow for Linux Mint / Headless servers
# ==============================================================================

set -e

INSTALL_DIR="$HOME/.local/share/screen-matrix"
BIN_DIR="$HOME/.local/bin"

echo "🚀 Installing Hesland ScreenMatrix (Terminal-Only Edition)..."

# 1. Create target directories
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$HOME/.config/screen-matrix"

# 2. Copy source files (excluding GUI desktop entries)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/bin" "$INSTALL_DIR/"

# 3. Mark executable and symlink
chmod +x "$INSTALL_DIR/bin/screen-matrix"
ln -sf "$INSTALL_DIR/bin/screen-matrix" "$BIN_DIR/screen-matrix"

# 4. Bind shortcuts hook scripts
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

# Ensure PATH is exported in user shells
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ]; then
        grep -q 'local/bin' "$rc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
    fi
done

if [ -f "$HOME/.zshenv" ]; then
    grep -q 'local/bin' "$HOME/.zshenv" || echo 'path+=($HOME/.local/bin)' >> "$HOME/.zshenv"
fi

echo "✅ Terminal-Only installation complete!"
echo "👉 Run 'screen-matrix' to launch the interactive terminal TUI dashboard"
echo "👉 Run 'screen-matrix 1|2|3' for instant headless mode switching"
