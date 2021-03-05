# !/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
from dynopy.workspace.workspace import Workspace
from dynopy.agents.lineFollwer2D import LineFollower2D
from dynopy.agents.volunteer2D import Volunteer2D


def load_workspace(filename, base_folder):
    file = os.path.join(base_folder, 'settings', filename)
    bound, e_params, positions = read_workspace_file(file)
    ws = Workspace(bound, e_params, positions)
    ws.generate_initial_distribution()
    return ws


def read_workspace_file(filename):

    with open(filename, 'r', encoding='utf8') as fin:
        reader = csv.reader(fin, skipinitialspace=True, delimiter=',')
        title = next(reader)[0]

        while title != '----':
            if title == 'boundary':
                boundary = []

                line = next(reader)
                while line[0] != '----':

                    coord = [int(x) for x in line]
                    boundary.append(tuple(coord))

                    line = next(reader)

            elif title == 'guassians':
                e_params = []
                keys = next(reader)

                line = next(reader)
                while line[0] != '----':
                    params = {}
                    values = [float(x) for x in line]

                    for key, val in zip(keys, values):
                        params.update({key: val})

                    e_params.append(params)
                    line = next(reader)

            elif title == 'positions':
                positions = []

                line = next(reader)
                while line[0] != '----':
                    coord = [float(x) for x in line]
                    positions.append([tuple(coord)])

                    line = next(reader)

            else:
                print("ERROR: settings title: '{}' not found".format(title))
                break

            title = next(reader)[0]

    return boundary, e_params, positions


def load_volunteer(cfg, lamb=0.99, budget=60, t_limit=0.1, gamma=1, plot_full=False, name="Blinky"):
    """
    Creates a Volunteer2D object without a current position
    :param cfg: file with dictionary of default parameters
    :param lamb: float [0,1) for fusion preference
    :param budget: int for maximum steps volunteer can take
    :param t_limit: float greater than or equal to 0.1 for time taken to expand tree
    :param gamma: float [0, 1] for discount on future rewards
    :param plot_full:
    :param name: default parameters to use
    :return:
    """

    if lamb < 0:
        lamb = 0
        print("Warning: lambda set out of range [0.0, 0.99), setting to 0")
    elif lamb >= 1:
        lamb = 0.99
        print("Warning: lambda set out of range [0.0, 0.99), setting to 0.99")

    if t_limit < 0.1:
        t_limit = 0.1
        print("Warning: t_limit set to less than 0.1, setting to 0.1")

    if gamma < 0:
        gamma = 0.0
        print("Warning: gamma set out of range [0.0, 1.0], setting to 0")
    elif gamma > 1:
        gamma = 1.0
        print("Warning: gamma set out of range [0.0, 1.0], setting to 1.0")

    cfg_volunteer = cfg.load_agent_parameters(name)

    cfg_volunteer.update({"lambda": lamb})
    cfg_volunteer.update({"budget": budget})
    cfg_volunteer.update({"t_limit": t_limit})
    cfg_volunteer.update({"gamma": gamma})

    robot = Volunteer2D(name, cfg_volunteer, plot_full=plot_full)

    return robot


def load_agents(n, cfg, agent_names=None):
    """
    Creates 'n' LineFollower2D objects without a current position or path
    :param n: number of agents to create
    :param cfg: file with dictionary of default parameters
    :param agent_names: list of configuration names if specific configurations are desired
    :return:
    """
    robots = []
    possible_names = cfg.get_cfg_names(False)

    if not agent_names:
        agent_names = possible_names[0:n]

    else:
        for name in agent_names:
            if name not in possible_names:
                print("Warning: provided configuration name: '{}' not available, removing from simulation".format(name))

        agent_names = [x for x in agent_names if x in possible_names]

    for name in agent_names:
        robots.append(LineFollower2D(name))

    return robots


def load_parameter_file(filename, base_folder):
    file = os.path.join(base_folder, 'settings', filename)
    parameters = read_parameter_file(file)
    return parameters


def read_parameter_file(file):
    params_list = []
    with open(file, 'r', encoding='utf8') as fin:
        reader = csv.DictReader(fin, skipinitialspace=True)

        for row in reader:
            row.update({
                "lambda": float(row.get("lambda")),
                "budget": int(row.get("budget")),
                "t_limit": float(row.get("t_limit")),
                "gamma": float(row.get("gamma")),
                "n_agents": int(row.get("n_agents")),
                "n_runs": int(row.get("n_runs"))
            })

            params_list.append(row)

    return params_list


def write_results_to_file(file, data_list):

    if not os.path.isfile(file):
        with open(file, 'w', newline='') as fout:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()

            for row in data_list:
                writer.writerow(row)

    else:
        with open(file, 'a', newline='') as fout:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter=',')

            for row in data_list:
                writer.writerow(row)


def read_results_file(filename, base_folder):
    # TODO: this should also be able to read dynamic number of agents
    results_list = []
    file = os.path.join(base_folder, 'results', filename)

    with open(file, 'r', encoding='utf8') as fin:
        reader = csv.DictReader(fin, skipinitialspace=True)

        for row in reader:
            results = {}
            results.update({
                "I_Gained": float(row.get("I_Gained")),
                "I_Fused": float(row.get("I_Fused")),
                "param_set": int(row.get("param_set")),
                "run": int(row.get("run"))
            })

            results_list.append(results)

    return results_list


def read_parameter_sets_file(filename, base_folder):
    # TODO: this should also be able to read dynamic number of agents
    results_list = []
    file = os.path.join(base_folder, 'results', filename)

    with open(file, 'r', encoding='utf8') as fin:
        reader = csv.DictReader(fin, skipinitialspace=True)

        for row in reader:
            row.update({
                "lambda": float(row.get("lambda")),
                "budget": int(row.get("budget")),
                "t_limit": float(row.get("t_limit")),
                "gamma": float(row.get("gamma")),
                "n_agents": int(row.get("n_agents")),
                "n_runs": int(row.get("n_runs")),
                "param_set": int(row.get("param_set")),
            })

            results_list.append(row)

    return results_list


