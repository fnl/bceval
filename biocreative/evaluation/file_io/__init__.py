"""file_io

Content iterators for all input file types.

ACT results are simple boolean flags.
INT results are strings of the identifier.
IPT results are ordered tuples of both identifiers.

Created by Florian Leitner on 2009-10-21.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

from biocreative.evaluation import class_loader

def result_reader_factory(evaluation_type):
    "Return the appropriate reader for results."
    return class_loader("Result%sReader" % evaluation_type)

def gold_standard_reader_factory(evaluation_type):
    "Return the appropriate reader for the gold standard."
    return class_loader("Gold%sReader" % evaluation_type)
