# !/usr/bin/env python
# -*- coding: utf-8 -*-

import dynopy.tools.load as load
from config import config

def main():
    """
    TODO: load an environment

    :return:
    """
    ws = load.workspace(file_ws)
    volunteer = load.volunteer(config, lamb, budget, t_limit, gamma)
    agents = load.agents(budget, file_agents)


if __name__ == "__main__":
    main()