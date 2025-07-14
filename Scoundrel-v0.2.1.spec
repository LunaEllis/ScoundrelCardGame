# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['scoundrel.py'],
    pathex=[],
    binaries=[],
    datas=[('data/classic_deck.json', 'data/'), ('demo_assets/scripts/console.py', 'demo_assets/scripts/'), ('demo_assets/scripts/classic_mode.py', 'demo_assets/scripts/'), ('demo_assets/lang/console_format_codes.json', 'demo_assets/lang/'), ('demo_assets/lang/en.json', 'demo_assets/lang/')],
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
    name='Scoundrel-v0.2.1',
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
)
