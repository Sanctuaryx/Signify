# signify.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['signify.py'],  # Asegúrate de que 'signify.py' sea el nombre del archivo principal correcto
    pathex=['.'],
    binaries=[],
    datas=[
        ('controllers/*', 'controllers'),
        ('services/*', 'services'),
        ('classes/*', 'classes'),
        ('repositories/*', 'repositories'),
        ('resources/SQL/int_dataBase/gestures.db', 'resources/SQL/int_dataBase/'),
        ('.venv/*', '.venv'),
        ('.venv/Lib/site-packages/TTS/*', 'TTS'),
        ('.venv/Lib/site-packages/TTS/config/*', 'TTS/config'),
        ('.venv/Lib/site-packages/TTS/bin/*', 'TTS/bin'),
        ('.venv/Lib/site-packages/trainer/*', 'trainer'),
    ],
    hiddenimports=[
        'controllers.bno055_controller',
        'repositories.gesture_repository',
        'services.calibration_service',
        'services.text_to_speech_service',
        'services.file_management_service',
        'services.gesture_service',
        'services.gesture_mapper_service',
        'classes.StaticGesture',
        'classes.GestureFactory',
        'classes.DynamicGesture',
        'classes.BaseGesture',
        'classes.AbstractGestureFactory',
        'TTS.api',
        'pyttsx3',
        'numpy',
        'scipy',
        'trainer',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='signify',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='signify')
