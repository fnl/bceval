"""map_filter

Homonym ortholog mapping and organism filtering logic. These classes extend
the standard containers.

Created by Florian Leitner on 2009-10-21.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from biocreative.evaluation import class_loader

def map_filter_factory(evaluation_type):
    return class_loader("%sDataDict" % evaluation_type)

