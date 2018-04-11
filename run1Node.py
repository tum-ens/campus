import os
import pandas as pd
import pyomo.environ
import shutil
import urbs
from pyomo.opt.base import SolverFactory


if __name__ == '__main__':
    input_file = '1Node.xlsx'
    result_name = os.path.splitext(input_file)[0]  # cut away file extension
    result_dir = urbs.prepare_result_directory(result_name)  # name+time stamp

    # copy input file to result directory
    shutil.copyfile(input_file, os.path.join(result_dir, input_file))
    # copy runme.py to result directory
    # shutil.copyfile(__file__, os.path.join(result_dir, __file__))

    # Choose Solver (cplex, glpk, gurobi, ...)
    Solver = 'glpk'

    # simulation timesteps
    (offset, length) = (3000, 168)  # time step selection
    timesteps = range(offset, offset+length+1)

    # plotting commodities/sites
    plot_tuples = [
        ('Campus', 'Elec'),
        ('Campus', 'Heat'),
        ('Campus', 'Cold')
    ]

    # detailed reporting commodity/sites
    report_tuples = [
        ('Campus', 'Elec'), ('Campus', 'Heat'), ('Campus', 'Cold')]

    # optional: define names for sites in report_tuples
    report_sites_name = {}

    # optional: define names for sites in plot_tuples
    plot_sites_name = {}

    # plotting timesteps
    plot_periods = {
        'spr': range(1000, 1000+24*7),
        'sum': range(3000, 3000+24*7),
        'aut': range(5000, 5000+24*7),
        'win': range(7000, 7000+24*7)
    }

    # add or change plot colors
    my_colors = {
        'South': (230, 200, 200),
        'Mid': (200, 230, 200),
        'North': (200, 200, 230)}
    for country, color in my_colors.items():
        urbs.COLORS[country] = color

    # select scenarios to be run
    scenarios = [
                 urbs.scenario_base,
                 urbs.sc_CO2limit(40000),
                 urbs.sc_1proprop('Campus', 'PVS30', 'inv-cost', 600000)
    ]

    for scenario in scenarios:
        prob = urbs.run_scenario(input_file, Solver, timesteps, scenario,
                            result_dir,
                            plot_tuples=plot_tuples,
                            plot_sites_name=plot_sites_name,
                            plot_periods=plot_periods,
                            report_tuples=report_tuples,
                            report_sites_name=report_sites_name)
