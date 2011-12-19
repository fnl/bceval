import logging

class AbstractEvaluator(object):
    """Abstract implementation of the evaluation process."""
    
    def __init__(self, cutoff, min_conf=0.0):
        self.cutoff = cutoff
        self.min_conf = min_conf
        self.primary_eval = None # micro for INT/IPT, AUC P/R for ACT
        self.secondary_eval = None # macro for INT/IPT, MCC+Acc for ACT
        self.results = None
        self.gold_standard = None
        self.logger = logging.getLogger("AbstractEvaluator")
        self.reset()
    
    def reset(self):
        """Reset the internal state to reuse the evaluator.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    # =============================================
    # = Main Entry Method into Evaluation Process =
    # =============================================
    def process(self, results, gold_standard):
        """Run the evaluation process for a result and GS data dictionary.
        
        This is the main entry method into the evaluation process.
        
        Return the primary (main) and secondary evaluation object:
        ACT, primary: AUC iP/R Evaluation
        ACT, secondary: Accuracy/MCC Evaluation
        INT/IPT, primary: macro-averaged Evaluation
        INT/IPT, secondary: micro-averaged Evaluation
        """
        self.logger.info("processing results with cutoff=%i" % self.cutoff)
        self.results = results
        self.gold_standard = gold_standard
        
        self._prepare()
        self._process()
        return self.primary_eval, self.secondary_eval
    
    def _prepare(self, results, gold_standard):
        """Prepare the instance for the evaluation run.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def _process(self):
        """Evaluate the individual performance for the given article.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def _process_doi(self, doi):
        """Evaluate the individual performance for the given article.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
