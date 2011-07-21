# encoding: utf-8
"""graphics

NB: Requires matplotlib installed!
Plot the AUC iP/R curve.

Created by Florian Leitner on 2009-10-28.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from settings import Evaluate

def plot_ipr_curves(evaluation_data, evaluation_type):
    "Plot the given evaluation object for the given data/evaluation type."
    # ==================================
    # = REQUIRES matplotlib INSTALLED! =
    # ==================================
    from matplotlib import pyplot
    ipr_values = evaluation_data.get_interpolated_pr_list()
    pr_values = tuple(evaluation_data.yield_precision_recall_pairs())
    handles = []
    labels = []
    
    handles.append(add_interpolated_curve(
        evaluation_type, zip(*ipr_values)
    ))
    labels.append("interpolated")
    
    if evaluation_type is Evaluate.ACT:
        handles.append(add_base_curve(zip(*pr_values)))
        labels.append("base")
    else:
        handles.append(add_scatter_plot(zip(*pr_values)))
        labels.append("overall, per rank")
    
    pyplot.xlim(0.0, 1.0)
    pyplot.ylim(0.0, 1.0)
    
    pyplot.legend(
        handles, labels,
        title="AUC iP/R: %.5f" % evaluation_data.auc_ipr,
        shadow=True
    )
    
    pyplot.show()

def insert_points(pr_values):
    p_values = list(pr_values[0])
    r_values = list(pr_values[1])
    
    if r_values[0] != 0.0:
        p_values.insert(0, p_values[0])
        r_values.insert(0, 0.0)
    
    if r_values[-1] != 1.0:
        r_values.append(r_values[-1])
        p_values.append(0.0)
    
    return p_values, r_values

def add_interpolated_curve(evaluation_type, pr_values):
    from matplotlib import pyplot
    pr_values = insert_points(pr_values)
    return pyplot.step(
        pr_values[1], pr_values[0], color="blue",
        linewidth=3 if evaluation_type is Evaluate.ACT else 1
    )

def add_scatter_plot(pr_values):
    from matplotlib import pyplot
    return pyplot.scatter(pr_values[1], pr_values[0], s=2, color="red")

def add_base_curve(pr_values):
    from matplotlib import pyplot
    # pr_values = insert_points(pr_values)
    return pyplot.plot(pr_values[1], pr_values[0], color="red")

