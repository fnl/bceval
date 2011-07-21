"""container

Data containers for the result and GS annotations; takes care of the sorting
of the results.

Created by Florian Leitner on 2009-10-21.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from biocreative.evaluation import class_loader
from biocreative.evaluation.settings import Evaluate

def container_factory(evaluation_type):
    if evaluation_type == Evaluate.ACT:
        return class_loader("ArticleDataDict")
    else:
        return class_loader("ProteinDataDict")
