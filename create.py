import shutil
from pathlib import Path

from importlib.resources import files
template_dir = files('apkp') / 'template'

def create_dirs(project_name : str):
    Path(project_name).mkdir(parents=True, exist_ok=True)
    Path(f'{project_name}/res/layout').mkdir(parents=True, exist_ok=True)
    Path(f'{project_name}/res/values').mkdir(parents=True, exist_ok=True)
    Path(f'{project_name}/src/com/{project_name}').mkdir(parents=True, exist_ok=True)

def create_files(project_name : str, app_name : str):
    src_dest_list = [
        ('AndroidManifest.xml', f'{project_name}/AndroidManifest.xml'),
        ('main.xml', f'{project_name}/res/layout/main.xml'),
        ('styles.xml', f'{project_name}/res/values/styles.xml'),
        ('MainActivity.kt', f'{project_name}/src/com/{project_name}/MainActivity.kt')
    ]

    for src, dest in src_dest_list:
        content = (template_dir / src).read_text()
        content = content.replace('{{pkgname}}', f'com.{project_name}')
        content = content.replace('{{appname}}', app_name)

        with open(dest, 'w') as file:
            file.write(content)

def create_project(project_name : str, app_name : str):
    create_dirs(project_name)
    create_files(project_name, app_name)