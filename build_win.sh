# This requires pyinstaller and can be ran on Windows in Git Bash
pyinstaller \
    --onefile \
    --windowed \
    --clean \
    --noconfirm \
    --add-data="templates;templates" \
    --add-data="static;static" \
    --exclude-module=config \
    --name vidify-web \
    gui_main.py
