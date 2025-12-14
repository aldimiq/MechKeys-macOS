from setuptools import setup

APP = ['app.py']
DATA_FILES = ['sound', 'menubar_icon_Template.png']
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'MechKeys.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': 'MechKeys',
        'CFBundleDisplayName': 'MechKeys',
        'CFBundleIdentifier': 'com.aldi.mechkeys',
        'CFBundleVersion': "0.4.0",
        'CFBundleShortVersionString': "0.4.0",
    },
    'packages': ['rumps', 'pynput', 'pygame'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)