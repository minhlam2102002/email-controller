import PyInstaller.__main__
PyInstaller.__main__.run([
    'app.py',
    '--onefile',
    '--noconsole',
    '--icon=app_icon.ico',
    '--name=app',
    '--key=trankieuminhlam1',
])