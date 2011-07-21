"""controller

Contollers for the process of evaluating a result set. Make sure that once
all objects are initialized and loaded to their correct state the evalution
is processed in the forseen order.

Created by Florian Leitner on 2009-10-21.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from biocreative.evaluation import class_loader
from biocreative.evaluation.settings import Evaluate

def controller_factory(evaluation_type):
    if evaluation_type == Evaluate.ACT:
        return class_loader("ArticleEvaluator")
    else:
        return class_loader("ProteinEvaluator")
