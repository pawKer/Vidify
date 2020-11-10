# This requires pyinstaller
pyinstaller \
    --windowed \
    --clean \
    --add-data="templates:templates" \
    --add-data="static:static" \
    --exclude-module=config \
    --name vidify \
    gui_main.py
