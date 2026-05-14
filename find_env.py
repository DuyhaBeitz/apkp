import os

def check_env_path(env_var) -> str:
    path = os.getenv(env_var)
    if (path == None):
        print(f'NOT FOUND {env_var}')
    else:
        print(f'FOUND {env_var}')
    return path