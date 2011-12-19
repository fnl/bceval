# encoding: utf-8
"""settings

Configuration constants.

Created by Florian Leitner on 2009-10-21.
Copyright (c) 2009 CNIO. All rights reserved.
License: GNU Public License, latest version.
"""

import logging
import os.path as p

class Defaults(object):
    "Global program defaults."
    
    SKIP_EMPTY_RESULTS = False
    PLOT_RESULT = False
    RESULT_ORDER = 11 # 001->conf; 010->rank; 100->line order
    # the three flags can be combined, the latter taking precedence over
    # the former; however, if conf or rank are given, the fields must be in
    # the result file - or, vice versa, absent in the file if not given
    CUTOFF_AT_RANK = 0 # 0 for no cutoff
    MIN_CONF = 0.0 # minimum confidence cutoff
    FIELD_SEPARATOR = '\t' # cannot be changed on the CL
    CONFIG_FILE = p.join(p.dirname(p.abspath(__file__)), 'configuration.ini')

class Evaluate(object):
    "Evaluation types handled by this library."
    
    ACT = 'ACT'
    INT = 'INT'
    IPT = 'IPT'
    IMT = 'INT'
    
    @staticmethod
    def check_type(evaluation):
        if evaluation in dir(Evaluate):
            return evaluation
        
        logging.error("unknown evaulation type '%s'" % str(evaluation))
        return Evaluate.INT
    
