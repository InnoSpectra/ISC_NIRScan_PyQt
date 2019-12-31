import sys
from cx_Freeze import setup, Executable

VERSION='1.0'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("ISC_PY_Program.py",
                          base=base,
                          targetName='DLP-NIR-SDK-PY.exe',
                          copyright="Copyright (C) 2019 InnoSpectra Corporation",
                          )]
build_exe_options = {
        'includes':['Forms/config_ui',
                    'Forms/devicelist',
                    'Forms/devices_ui',
                    'Forms/main_ui',
                    'Forms/mainwindow',
                    'Forms/scanconfigdialog',
                    'SDK/device',
                    'SDK/scan',
                    'SDK/scanconfig'
                    ],
        'include_files':['SDK/hidapi.dll',
                         'SDK/iscpy.cp36-win32.pyd',
                         'SDK/iscpy.pyd',
                         'SDK/libdlpspec.dll',
                         'SDK/lmdfu.dll',
                         'SDK/lmusbdll.dll']
                     }

# build_msi_options = {'add_to_path': False,
#                      'initial_target_dir': r'[C:\\LibraryBuilder]'}

options = {
    'build_exe':build_exe_options,
    # 'bdist_msi':build_msi_options,
}

setup(
    name = "DLP-NIR-SDK-PY",
    options = options,
    version = VERSION,
    description = 'Demonstration ISC python SDK',
    executables = executables
)