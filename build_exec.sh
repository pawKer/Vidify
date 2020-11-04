pyinstaller \
    --onefile --windowed \
    --clean \
    --add-data="templates:templates" \
    --add-data="static:static" \
    --exclude-module=config \
    --icon="icon.ico" \
    --name vidify \
    server.py
