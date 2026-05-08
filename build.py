import json
import subprocess
import os

from pathlib import Path

def check_env_path(env_var) -> str:
    path = os.getenv(env_var)
    if (path == None):
        print(f'NOT FOUND {env_var}')
    else:
        print(f'FOUND {env_var}')
    return path


def build():
    build_dest = 'apkp_build'

    # create template tree structure
    Path(f'{build_dest}/compiled_res').mkdir(parents=True, exist_ok=True)
    Path(f'{build_dest}/src').mkdir(parents=True, exist_ok=True)
    Path(f'{build_dest}/classes').mkdir(parents=True, exist_ok=True)
    Path(f'{build_dest}/dex').mkdir(parents=True, exist_ok=True)

    # find JDK and AndroidSDK
    JDK = check_env_path('JAVA_HOME')
    AndroidSDK = check_env_path('ANDROID_HOME')

    if (JDK == None or AndroidSDK == None): return

    # pick android version
    available_android_versions = []
    for item in Path(f'{AndroidSDK}/platforms').iterdir():
        path = str(item)
        folder_name = path.split('/')[-1]
        android_version = folder_name.split('-')[-1]
        available_android_versions.append(int(android_version))
    
    print('Available android versions:', *available_android_versions)

    android_version = int(input(f'Input android version: '))
    if android_version not in available_android_versions:
        print(f'incorrect android version')
        return
    
    android_path = f'{AndroidSDK}/platforms/android-{android_version}'

    # find build-tools path    
    build_tools_path = None
    for item in Path(f'{AndroidSDK}/build-tools').iterdir():
        path = str(item)
        if str(android_version) in path:
            build_tools_path = path
            break

    if build_tools_path == None:
        print("didn't find build tools for this android version")
        return

    #print(f'{android_path=}')
    #print(f'{build_tools_path=}')

    aapt2 = f'{build_tools_path}/aapt2'
    d8 = f'{build_tools_path}/d8'
    zipalign = f'{build_tools_path}/zipalign'
    apksigner = f'{build_tools_path}/apksigner'

    kotlinc_dir = subprocess.run('dirname "$(dirname "$(which kotlinc)")"', shell=True, capture_output=True, text=True).stdout.strip()
    kotlinc = f'{kotlinc_dir}/bin/kotlinc'
    kotlinc_stdlib = f'{kotlinc_dir}/lib/kotlin-stdlib.jar'

    print("Building recources...")
    subprocess.run(f'{aapt2} compile --dir res/ -o {build_dest}/compiled_res/', shell=True)

    print("Linking recources...")
    subprocess.run(f'{aapt2} link -o {build_dest}/resources.ap_\
                    --manifest AndroidManifest.xml \
                    -R {build_dest}/compiled_res/*.flat \
                    --java {build_dest}/src/ \
                    -I {android_path}/android.jar', shell=True)
    
    print("Compiling kotlin source...")
    subprocess.run(f'{kotlinc} -classpath "{android_path}/android.jar" \
                    -d {build_dest}/classes \
                    $(find src {build_dest}/src -name "*.kt" -o -name "*.java")', shell=True)
    

    print("Converting compiled kotlin into dex...")
    subprocess.run(f'{d8} --output {build_dest}/dex \
                    --lib "{android_path}/android.jar" \
                    --lib "{kotlinc_stdlib}" \
                    $(find {build_dest}/classes -name "*.class")', shell=True)


    print(f'Building final APK inside {build_dest}...')
    subprocess.run(f'{aapt2} link -o {build_dest}/my_app_unsigned.apk \
                    -I {android_path}/android.jar \
                    --manifest AndroidManifest.xml \
                    -R $(find {build_dest}/compiled_res -name "*.flat")', shell=True)

    print("Adding DEX to APK...")
    subprocess.run(f'zip -j -u {build_dest}/my_app_unsigned.apk {build_dest}/dex/*.dex', shell=True)

    print('Aligning APK...')
    subprocess.run(f'{zipalign} -v -p 4 {build_dest}/my_app_unsigned.apk {build_dest}/my_app_aligned.apk', shell=True)

    if not Path("my-release-key.jks").exists():
        print('No signing key found. Creating signing key...')
        subprocess.run('keytool -genkeypair -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias', shell=True)
    else:
        print('Using existing signing key')

    print('Signing APK...')
    subprocess.run(f'{apksigner} sign --ks my-release-key.jks --out {build_dest}/my_app_signed.apk {build_dest}/my_app_aligned.apk', shell=True)

