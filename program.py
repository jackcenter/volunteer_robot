# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os



def main():
    working = True

    while working:
        print_header()
        cmd = get_user_input()
        working = interpret_command(cmd)


def print_header():
    print('---------------------------------------------------')
    print('                    COHRINT')
    print('              The Volunteer Robot ')
    print('                  Jack Center ')
    print('---------------------------------------------------')
    print()


def get_user_input():
    print('Select from the following programs:')
    print(' [1]: Single Simulation')
    print(' [2]: Benchmarking')
    print(' [3]: Test Environment')
    print(' [q]: Quit')
    print()
    print(' NOTE: parameters for the workspace and agents can be changed in the settings files.')
    print()

    cmd = input(' Select an exercise would you like to run: ')
    print()

    cmd = cmd.strip().lower()

    return cmd


def interpret_command(cmd):
    if cmd == '1':
        os.system("python simulation_options_menu.py single")

    elif cmd == '2':
        os.system("python simulation_options_menu.py benchmark")

    elif cmd == '3':
        status = os.system("python environment_test.py")

    elif cmd == 'q':
        print(" closing program ... goodbye!")
        return False

    else:
        print(' ERROR: unexpected command...')
        run_again = input(' Would you like to run another program?[y/n]: ')
        print()

        if run_again != 'y':
            print(" closing program ... goodbye!")
            return False

    return True


if __name__ == '__main__':
    main()
