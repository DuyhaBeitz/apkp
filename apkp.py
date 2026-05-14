#!/usr/bin/env python3
import sys
import create
import build
import test

def print_help():
    print('Commands [no additional arguments]:')
    print('\tcreate')
    print('\tbuild')
    print('\ttest')

def main():
    if (len(sys.argv) != 2):
        print('Wrong number of arguments')
        print_help()
    else:
        if sys.argv[1] == 'create':
            project_name = input("enter project name (default= myapp): ")
            if project_name == '': project_name = 'myapp'

            app_name = input("enter app name (default= My App): ")
            if app_name == '': app_name = 'My App'

            create.create_project(project_name, app_name)
        elif sys.argv[1] == 'build':
            build.build()
        elif sys.argv[1] == 'test':
            test.test()
        else:
            print(f'uknown command "{sys.argv[1]}"')

if __name__ == "__main__":
    main()