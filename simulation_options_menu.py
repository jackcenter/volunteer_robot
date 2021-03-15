# !/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import sys
import matplotlib.pyplot as plt
from dynopy.tools.initialize import load_parameter_file, write_results_to_file
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
    print(' [3]: Display Previous Result')
    print(' [4]: Static Agents, Separated, In the Info, with a single Mode')
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

    elif cmd == '4':
        filename_ws = 'static_separated_collocated_single.txt'
        filename_params = "parameters_sandbox.txt"
        params_list = load_parameter_file(filename_params, os.path.dirname(__file__))
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
        environment_name = 'static_single'
        filename_ws = 'static_separated_void_single.txt'
        filename_params = "parameters_benchmark.txt"
        params_list = load_parameter_file(filename_params, os.path.dirname(__file__))

    elif cmd == '2':
        environment_name = 'sandbox'
        filename_ws = 'workspace_sandbox.txt'
        file_params = "parameters_benchmark.txt"
        params_list = load_parameter_file(file_params, os.path.dirname(__file__))

    elif cmd == '3':
        results_filename = "static_single_results.txt"
        params_filename = "static_single_parameter_sets.txt"
        plot_comparison(results_filename, params_filename, "gamma", ["I_Gained", "I_Fused"])
        plt.show()

        results_filename_2 = "archive/static_single_results_r2.txt"
        params_filename_2 = "archive/static_single_parameter_sets_r2.txt"

        plot_box(results_filename_2, params_filename, "gamma", "I_Fused")

        plot_box(results_filename_2, params_filename, "gamma", "I_Gained")
        plt.show()
        plt.close()

        plot_box(results_filename_2, params_filename_2, "lambda", "I_Fused")

        plot_box(results_filename_2, params_filename_2, "lambda", "I_Gained")
        plt.show()


        # plot_comparison(results_filename_2, params_filename_2, "gamma", ["I_Gained", "I_Fused"])
        # plt.show()

        # plot_comparison(results_filename_2, params_filename_2, "lambda", ["I_Gained", "I_Fused", "Inky_Fused", "Clyde_Fused"])
        # plt.show()

        # plot_comparison_dual(results_filename, params_filename, results_filename_2, params_filename_2, "lambda", ["I_Gained"])
        # plt.show()

        return

    elif cmd == '4':
        environment_name = 'static_collocated'
        filename_ws = 'static_separated_collocated_single.txt'
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
        results_filename = environment_name + '_results.txt'
        params_filename = environment_name + '_parameter_sets.txt'

        results_file = os.path.join(os.path.dirname(__file__), 'results', results_filename)
        params_file = os.path.join(os.path.dirname(__file__), 'results', params_filename)

        n_params = len(params_list)
        p_run = 0

        for params in params_list:
            p_run += 1
            p, new_param = identify_params(params, params_file)

            params.update({"param_set": p})
            runs = params.get("n_runs")

            if new_param:
                write_results_to_file(params_file, [params])

            for r in range(0, runs):

                print(" Parameter Set: {} of {}\t\tRun: {} of {} ".format(p_run, n_params, r + 1, runs), end='\r')
                results = single_simulation.run(
                    filename_ws,
                    params.get("lambda"),
                    params.get("budget"),
                    params.get("t_limit"),
                    params.get("gamma"),
                    params.get("n_agents"),
                    False,
                    False
                )

                results.update({"param_set": p, "run": r})
                write_results_to_file(results_file, [results])

        x, y = get_results("lambda", "I_Gained", params_file, results_file)

        plt.close()
        f, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()

        print()

    return working


def print_results(results_list, params_list, variable):
    totals = {}
    params = {}

    for result in results_list:
        param_set = result.get("param_set")

        if not params.get(param_set):
            for set in params_list:
                if set.get("param_set") == param_set:
                    params.update({param_set: set})
                    break

        if not totals.get(param_set):
            totals.update({param_set: [0.0, 0.0]})

        vals_0 = totals.get(param_set)
        vals = [result.get("I_Gained"), result.get("I_Fused")]

        totals.update({param_set: [vals_0[i] + vals[i] for i in range(len(vals_0))]})

    for key, val in totals.items():
        x = params.get(key).get(variable)
        gained = round(val[0], 4)
        fused = round(val[1], 4)
        print("Set: {}\t{}: {}\t{}, {}\t-- I_Gained, I_Fused".format(key, variable, x, gained, fused))
    print()
    input("Continue?")


# noinspection PyTypeChecker
def identify_params(params, file):

    param_id = None
    param_id_max = 0        # assigns 0 unless a param set is found
    new_param = False

    if not os.path.isfile(file):
        # file doesn't exist, so neither does a parameter set
        param_id = 1
        new_param = True

    else:
        with open(file, 'r', encoding='utf8') as fin:
            reader = csv.DictReader(fin, skipinitialspace=True)

            for row in reader:
                # see if parameter is in results set already
                row.update({
                    "lambda": float(row.get("lambda")),
                    "budget": int(row.get("budget")),
                    "t_limit": float(row.get("t_limit")),
                    "gamma": float(row.get("gamma")),
                    "n_agents": int(row.get("n_agents")),
                    "n_runs": int(params.get("n_runs")),    # doesn't need to be identical
                    "param_set": int(row.get("param_set"))
                })

                param_id_row = int(row.get("param_set"))
                params.update({"param_set": param_id_row})

                if params == row:
                    # param set found
                    param_id = param_id_row
                    break

                elif param_id_row > param_id_max:
                    # param set not found
                    param_id_max = param_id_row

    if not param_id:
        param_id = param_id_max + 1
        new_param = True

    return param_id, new_param


# noinspection PyTypeChecker
def get_results(x_key, y_key, x_file, y_file):
    x_list = []
    y_list = []

    with open(x_file, 'r', encoding='utf8') as fin_x:
        reader_x = csv.DictReader(fin_x, skipinitialspace=True)

        for row_x in reader_x:
            x_list.append(float(row_x.get(x_key)))
            param_set = row_x.get("param_set")

            y_vals = []
            with open(y_file, 'r', encoding='utf8') as fin_y:
                reader_y = csv.DictReader(fin_y, skipinitialspace=True)

                for row_y in reader_y:
                    if row_y.get("param_set") == param_set:
                        y_vals.append(float(row_y.get(y_key)))

                y_list.append(sum(y_vals)/len(y_vals))

    return x_list, y_list


def get_results_full(x_key, y_key, x_file, y_file):
    x_list = []
    y_list = []

    with open(x_file, 'r', encoding='utf8') as fin_x:
        reader_x = csv.DictReader(fin_x, skipinitialspace=True)

        for row_x in reader_x:
            x_list.append(float(row_x.get(x_key)))
            param_set = row_x.get("param_set")

            y_vals = []
            with open(y_file, 'r', encoding='utf8') as fin_y:
                reader_y = csv.DictReader(fin_y, skipinitialspace=True)

                for row_y in reader_y:
                    if row_y.get("param_set") == param_set:
                        y_vals.append(float(row_y.get(y_key)))

                y_list.append(y_vals)

    return x_list, y_list


def plot_comparison(results_filename, params_filename, x_key, y_keys):

    results_file = os.path.join(os.path.dirname(__file__), 'results', results_filename)
    params_file = os.path.join(os.path.dirname(__file__), 'results', params_filename)

    plt.close()
    f, ax = plt.subplots()

    for y_key in y_keys:
        x, y = get_results(x_key, y_key, params_file, results_file)
        ax.plot(x, y, 'o')

    ax.set_title(x_key + " vs " + y_keys[0])
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_keys[0])


def plot_box(results_filename, params_filename, x_key, y_key):

    results_file = os.path.join(os.path.dirname(__file__), 'results', results_filename)
    params_file = os.path.join(os.path.dirname(__file__), 'results', params_filename)

    x, y = get_results_full(x_key, y_key, params_file, results_file)
    zipped_lists = zip(x, y)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    x_new, y_new = [list(i) for i in tuples]
    points = range(1, len(x_new) + 1)

    f, ax = plt.subplots()
    ax.boxplot(y_new)
    ax.set_title(x_key + " vs " + y_key)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)

    plt.xticks(points, x_new)


def plot_comparison_dual(rfn1, pfn1, rfn2, pfn2, x_key, y_keys):

    results_file_1 = os.path.join(os.path.dirname(__file__), 'results', rfn1)
    params_file_1 = os.path.join(os.path.dirname(__file__), 'results', pfn1)

    results_file_2 = os.path.join(os.path.dirname(__file__), 'results', rfn2)
    params_file_2 = os.path.join(os.path.dirname(__file__), 'results', pfn2)

    plt.close()
    f, ax = plt.subplots()

    legend_entries = []
    for y_key in y_keys:
        x1, y1 = get_results(x_key, y_key, params_file_1, results_file_1)
        x2, y2 = get_results(x_key, y_key, params_file_2, results_file_2)
        ax.plot(x1, y1, x2, y2)
        legend_entries.append([y_key + "_1"])
        legend_entries.append([y_key + "_2"])

    ax.set_title("Lambda vs Information")
    ax.set_xlabel("Lambda")
    ax.set_ylabel("Information")
    ax.legend(y_keys)


def update_dict_types(row):
    row.update({
        "lambda": float(row.get("lambda")),
        "budget": int(row.get("budget")),
        "t_limit": float(row.get("t_limit")),
        "gamma": float(row.get("gamma")),
        "n_agents": int(row.get("n_agents")),
        "n_runs": int(row.get("n_runs"))
    })


if __name__ == '__main__':
    main()
