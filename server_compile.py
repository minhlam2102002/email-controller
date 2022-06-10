import PyInstaller.__main__

PyInstaller.__main__.run([
    'server.py',
    '--onefile',
    '--icon=server_icon.ico',
    '--name=server',
    '--key=trankieuminhlam1',
])