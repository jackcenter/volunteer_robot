# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
from dynopy.tools.initialize import load_parameter_file
import single_simulation


def main():
    simulation_type = sys.argv[1]

    working = True

    while working:
        print_header(simulation_type)
        cmd = get_user_input()
        working = interpret_command(cmd, simulation_type)


def print_header(sim_type):
    if sim_type == 'single':
        line = '               Single Simulation'
    elif sim_type == 'benchmark':
        line = '              Benchmark Simulation'

    print('---------------------------------------------------')
    print(line)
    print('---------------------------------------------------')
    print()


def get_user_input():
    print('Select from the following programs:')
    print(' [1]: Static Agents, Separated, In a Void, with a Single Mode')
    print(' [2]: Sandbox')
    # print(' [3]: Environment 3')
    print(' [q]: Quit')
    print()

    cmd = input(' Select an exercise would you like to run: ')
    print()

    cmd = cmd.strip().lower()

    return cmd


def interpret_command(cmd, simulation_type):

    if simulation_type == 'single':
        working = interpret_single_sim_cmd(cmd)

    elif simulation_type == 'benchmark':
        working = interpret_benchmark_sim_cmd(cmd)

    else:
        print("Error: simulation type not understood")
        working = False

    return working


def interpret_single_sim_cmd(cmd):
    working = True
    filename_ws = None
    params = None

    if cmd == '1':
        filename_ws = 'static_separated_void_single.txt'
        filename_params = "parameters_sandbox.txt"
        params_list = load_parameter_file(filename_params, os.path.dirname(__file__))
        params = params_list[0]

    elif cmd == '2':
        filename_ws = 'workspace_sandbox.txt'
        file_params = "parameters_sandbox.txt"
        params_list = load_parameter_file(file_params, os.path.dirname(__file__))
        params = params_list[0]

    elif cmd == 'q':
        print(" returning to main menu")
        working = False

    else:
        print(' ERROR: unexpected command...')
        run_again = input(' Would you like to run another program?[y/n]: ')
        print()

        if run_again != 'y':
            print(" returning to main menu")
            working = False

    if working:
        results = single_simulation.run(filename_ws,
                                        params.get("lambda"),
                                        params.get("budget"),
                                        params.get("t_limit"),
                                        params.get("gamma"),
                                        params.get("n_agents"),
                                        True,
                                        False)

        for key, val in results.items():
            print(" {}:\t{}".format(key, val))

        print("\n")
        plt.show()

    return working


def interpret_benchmark_sim_cmd(cmd):
    working = True
    filename_ws = None
    params_list = None

    if cmd == '1':
        filename_ws = 'static_separated_void_single.txt'
        filename_params = "parameters_benchmark.txt"
        params_list = load_parameter_file(filename_params, os.path.dirname(__file__))

    elif cmd == '2':
        filename_ws = 'workspace_sandbox.txt'
        file_params = "parameters_benchmark.txt"
        params_list = load_parameter_file(file_params, os.path.dirname(__file__))

    elif cmd == 'q':
        print(" returning to main menu")
        working = False

    else:
        print(' ERROR: unexpected command...')
        run_again = input(' Would you like to run another program?[y/n]: ')
        print()

        if run_again != 'y':
            print(" returning to main menu")
            working = False

    if working:
        results_list = []
        n_params = len(params_list)
        p = 0
        for params in params_list:
            p += 1
            runs = params.get("n_runs")
            for i in range(0, runs):

                print(" Parameter Set: {} of {}\t\tRun: {} of {}".format(p, n_params, i + 1, runs), end='\r')
                results = single_simulation.run(filename_ws,
                                                params.get("lambda"),
                                                params.get("budget"),
                                                params.get("t_limit"),
                                                params.get("gamma"),
                                                params.get("n_agents"),
                                                False,
                                                False)

                results_list.append([params, i, results])

        print()

    return working


if __name__ == '__main__':
    main()
