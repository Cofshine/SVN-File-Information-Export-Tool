# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui', 'openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'PyQt5', 'PyQt6', 'tkinter', 'wx', 'pandas', 'PIL', 
             'numpy', 'scipy', 'test', 'unittest', 'pydoc', 'doctest',
             'pkg_resources', 'pdb', 'setuptools', 'distutils'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

def remove_from_binaries(binaries, substring):
    return [(name, path, type) for (name, path, type) in binaries if substring not in name.lower()]

a.binaries = remove_from_binaries(a.binaries, 'qwebengine')
a.binaries = remove_from_binaries(a.binaries, 'qml')
a.binaries = remove_from_binaries(a.binaries, 'qt6quick')
a.binaries = remove_from_binaries(a.binaries, 'qt6qml')
a.binaries = remove_from_binaries(a.binaries, 'qt6pdf')
a.binaries = remove_from_binaries(a.binaries, 'qt6designer')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SVN Exporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/app.ico'
) 
