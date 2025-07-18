# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['scoundrel.py'],
    pathex=[],
    binaries=[],
    datas=[('demo_assets/lang/console_format_codes.json', 'demo_assets/lang/'), ('demo_assets/lang/en.json', 'demo_assets/lang/'), ('demo_assets/scripts/classic_mode.py', 'demo_assets/scripts/'), ('demo_assets/scripts/colours_test.py', 'demo_assets/scripts/'), ('demo_assets/scripts/console.py', 'demo_assets/scripts/'), ('demo_assets/scripts/__pycache__', 'demo_assets/scripts/'), ('demo_assets/sprites/cards', 'demo_assets/sprites/'), ('data/classic_deck.json', 'data/'), ('data/saves', 'data/'), ('data/standard_deck.json', 'data/'), ('config.json', './')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Scoundrel-v0.2.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\AtHOM\\Documents\\- Python\\ScoundrelCardGame\\icon.ico'],
)
