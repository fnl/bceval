# encoding: utf-8
"""graphics

NB: Requires matplotlib installed!
Plot the AUC iP/R curve.

Created by Florian Leitner on 2009-10-28.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from settings import Evaluate

def plot_avrg_p_curves(evaluation_data, secondary_data, evaluation_type):
    "Plot the given evaluation object for the given data/evaluation type."
    # ==================================
    # = REQUIRES matplotlib INSTALLED! =
    # ==================================
    from matplotlib import pyplot
    pr_values = tuple(evaluation_data.yield_precision_recall_pairs())
    handles = []
    labels = []

    if evaluation_type == Evaluate.ACT:
        handles.append(add_pr_curve(zip(*pr_values)))
        labels.append("Precision/Recall")
        title = "AUC = %.4f" % evaluation_data.auc_pr
    else:
        pr2_values = tuple(secondary_data.yield_precision_recall_pairs())
        handles.append(add_avrg_p_curve(zip(*pr2_values), "blue"))
        labels.append("macro-avr. AUC = %.4f" % secondary_data.avrg_p)
        handles.append(add_avrg_p_curve(zip(*pr_values)))
        labels.append("micro-avr.  AUC = %.4f" % evaluation_data.avrg_p)
        title = "Average Precision"
        pr_values += pr2_values

    max_val = max((max(p for p, r in pr_values),
                   max(r for p, r in pr_values)))
    # axis = int(max_val * 10) + 3
    # if axis > 10: axis = 10
    # axis /= 10.0
    pyplot.ylim(0.0, 1.0)
    pyplot.xlim(0.0, 1.0)
    pyplot.legend(handles, labels, title=title, shadow=True)
    pyplot.show()

def insert_points(pr_values, avrg_p=False):
    p_values = list(pr_values[0])
    r_values = list(pr_values[1])
    
    if r_values[0] != 0.0:
        if avrg_p:
            p_values.insert(0, p_values[0])
        else:
            p_values.insert(0, 1.0)
        
        r_values.insert(0, 0.0)
    
    if avrg_p:
        to_delete = []
        last_r = r_values[0]
        val_len = len(r_values)
        
        for idx in range(1, val_len):
            if r_values[idx] == last_r:
                to_delete.append(idx)
            
            last_r = r_values[idx]
        
        to_delete.reverse()
        
        for idx in to_delete:
            del r_values[idx]
            del p_values[idx]
    
    if r_values[-1] != 1.0 or p_values[-1] != 0.0:
        r_values.append(r_values[-1])
        p_values.append(0.0)
    
    return p_values, r_values

def add_avrg_p_curve(pr_values, color="red"):
    from matplotlib import pyplot
    pr_values = insert_points(pr_values, True)
    return pyplot.step(pr_values[1], pr_values[0], color=color)

def add_pr_curve(pr_values):
    from matplotlib import pyplot
    pr_values = insert_points(pr_values)
    return pyplot.plot(pr_values[1], pr_values[0], color="red")

