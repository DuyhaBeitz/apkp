install:

python3 -m venv venv
./venv/bin/pip install .

then run:
venv/bin/apkp

just run:
python3 -m apkp.main


Commands:

create project - (command line menu where you specify pkg name etc. then it creates project template for you)

build project - (compiles resources with aapt2, links them, compiles sources with kotlinc, builds dex using d8, builds APK with appt2, signs APK with apksigner )

maybe also: deploy to connected android, test(using some emulator?)