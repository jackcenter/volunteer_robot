# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import single_simulation


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
    print(' [1]: Single Simulation - Holonomic')
    print(' [2]: Test Environment')
    # print(' [3]: Nonlinear Dynamics Simulation')
    print(' [q]: Quit')
    print()
    print(' NOTE: parameters for landmarks and dynamics models can be changed the configuration file.')
    print()

    cmd = input(' Select an exercise would you like to run: ')
    print()

    cmd = cmd.strip().lower()

    return cmd


def interpret_command(cmd):
    if cmd == '1':
        results = single_simulation.run('test.txt', 0.99, 75, 0.5, 1, True, True)

        for key, val in results.items():
            print("{}:\t{}".format(key, val))

        print("\n")
        plt.show()

    elif cmd == '2':
        status = os.system("python environment_test.py")


    elif cmd == '3':
        print(" Sorry, this section is not functional at this time")
        # status = os.system("python decentralized_data_fusion/UI_static_simulation.py")

    elif cmd == '4':
        print(" Sorry, this section is not functional at this time")
        # status = os.system("python target_search/UI_static_simulation.py")

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
