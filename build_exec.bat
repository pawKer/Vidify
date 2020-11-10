pyinstaller ^
    --onefile ^
    --clean ^
    --add-data=templates;templates ^
    --add-data=static;static ^
    --exclude-module=config ^
    --name vidify ^
    server.py
