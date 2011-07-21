import logging

from biocreative.evaluation.settings import Defaults, Evaluate

class Parameters(object):
    "Checks and stores parameters required to run the evaluation."
    
    def __init__(self, opts=Defaults):
        """Initialize a new parameter object."""
        # parameters
        self.field_separator = Defaults.FIELD_SEPARATOR
        self.evaluation_type = Evaluate.check_type(opts.EVALUATION_TYPE)
        self.cutoff = int(opts.CUTOFF_AT_RANK)
        
        # flags
        self.plot_result = bool(opts.PLOT_RESULT)
        self.skip_empty_results = bool(opts.SKIP_EMPTY_RESULTS)
        self.set_result_order(int(opts.RESULT_ORDER))
    
    def set_result_order(self, result_order):
        "Determine the ordering employed on the results given the parameters."
        self.result_order = result_order
        
        if self.result_order <= 0:
            logging.info(
                "no result ordering given, "
                "using rank and expecting confidence"
            )
            self.result_order = Defaults.RESULT_ORDER
        elif self.result_order > 99:
            logging.info(
                "results will be ordered by using the line order as rank"
            )
        elif self.result_order > 9:
            logging.info(
                "results will be ordered by rank"
            )
        else:
            logging.info(
                "results will be ordered by confidence"
            )

