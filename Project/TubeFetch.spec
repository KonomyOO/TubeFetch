# -*- mode: python ; coding: utf-8 -*-

import os
import flet # تأكد من استيراد flet هنا

block_cipher = None

# المسار إلى ملف main.py الخاص بتطبيق Flet
flet_app_path = 'main.py'

# الحصول على مسار أصول Flet الداخلية
flet_path = os.path.dirname(os.path.abspath(flet.__file__))
flet_assets_path = os.path.join(flet_path, 'client', 'public')

a = Analysis(
    [flet_app_path],
    pathex=['.'],
    binaries=[],
    datas=[
        # (flet_assets_path, 'flet_app/client/public'), # Removed as the directory was not found
    ],
    hiddenimports=['flet_core'], # تأكد من تضمين flet_core
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TubeFetch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # اجعلها False لتطبيق رسومي بدون نافذة طرفية
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TubeFetch',
)
