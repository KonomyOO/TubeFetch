# -*- mode: python ; coding: utf-8 -*-

import os
import flet 

block_cipher = None

flet_app_path = 'main.py'

# flet_path = os.path.dirname(os.path.abspath(flet.__file__))
# flet_assets_path = os.path.join(flet_path, 'client', 'public')

a = Analysis(
    [flet_app_path],
    pathex=['.'],
    binaries=[],
    datas=[
        # إذا أضفت أي ملفات غير برمجية (مثل صور، ملفات إعدادات) تحتاج إلى تضمينها، أضفها هنا.
        # مثال: ('path/to/your/image.png', '.'),
        #If you've added any non-code files (like images, configuration files) that need to be included, add them here.
        #example: ('path/to/your/image.png', '.'),
    ],
    hiddenimports=['flet_core'], # تأكد من تضمين flet_core!, Be sure to include flet_core.
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
    console=False, #  False لتطبيق رسومي بدون نافذة طرفية, False for a graphical application without a terminal window.
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
