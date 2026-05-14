import subprocess

from pathlib import Path

import find_env

import subprocess
import time

def wait_for_emulator_boot(adb, timeout_seconds=20):
    print("Waiting for device to appear...")
    subprocess.run(f'{adb} wait-for-device', shell=True, capture_output=True)
    
    print("Waiting for boot completion...")
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        result = subprocess.run(
            f'{adb} shell getprop sys.boot_completed',
            shell=True, capture_output=True, text=True
        )
        boot_completed = result.stdout.strip()
        
        if boot_completed == '1':
            print("Emulator boot completed")
            return True
        
        time.sleep(2)
    
    print("Timed out waiting for emulator to boot")
    return False

def test():
    if not Path('AndroidManifest.xml').is_file():
        print('not inside apkp anroid project')
        return

    current_dir = str(Path.cwd())
    project_name = current_dir.split('/')[-1]
    print(project_name)

    AndroidSDK = find_env.check_env_path('ANDROID_HOME')

    if (AndroidSDK == None): return

    emulator = f'{AndroidSDK}/emulator/emulator'
    avdmanager  = f'{AndroidSDK}/cmdline-tools/latest/bin/avdmanager'
    adb = f'{AndroidSDK}/platform-tools/adb'
   
    start_env = 'ANDROID_AVD_HOME="$HOME/.android/avd"'
    available_avds = subprocess.run(f'{start_env} {emulator} -list-avds', shell=True, capture_output=True, text=True).stdout.strip()
    available_avds = available_avds.split()
    print(available_avds)

    if 'TestAvd' not in available_avds:
        subprocess.run(f'{start_env} {avdmanager} create avd -n TestAvd -k "system-images;android-35;google_apis_playstore;x86_64" -d "pixel_6" --force', shell=True)

    emu_process = subprocess.Popen(f'{start_env} {emulator} -avd TestAvd', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    build_dest = 'apkp_build'
    if wait_for_emulator_boot(adb):
        subprocess.run(f'{adb} install -r -d {build_dest}/my_app_signed.apk', shell=True)
        subprocess.run(f'{adb} shell am start -n com.{project_name}/.MainActivity', shell=True)