# YourGameName.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['/Users/madan/Documents/Year 12 2024/Year 12 Computer Science ATAR/Forestfall/Forestfall'],
    binaries=[],
    datas=[
        ('/Users/madan/Documents/Year 12 2024/Year 12 Computer Science ATAR/Forestfall/Forestfall/data', 'data'),
        # Add more files as needed
    ],
    hiddenimports=[
        'your_additional_script1',
        'your_additional_script2',
        # Add more scripts as needed
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Forestfall',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want a console to appear
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Forestfall',
)
app = BUNDLE(
    coll,
    name='Forestfall.app',
    icon=None,
    bundle_identifier=None,
)
