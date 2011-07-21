import logging

from collections import defaultdict

import biocreative.evaluation.calculation.hits as hits

class AbstractEvaluation(object):
    """Container for a Hit set and a dictionary of recall values with lists
    of precision values found for them.
    
    This class implements most of the relevant calculations for the
    evaluation.
    """
    
    def __init__(self, doi=None, fn=None):
        """doi can be left to None for global results, and should be set to
        the value for per document results (only used for logging).
        
        The fn counter can be set to the appropriate value right during
        initialization (to the number of GS annotation).
        """
        self.logger = logging.getLogger("EvaluationData:%s" % str(doi))
        self.precisions_at_recall = defaultdict(set)
        self.hits = hits.Hits(fn=fn)
        self.doi = doi
    
    def evaluate(self, result_item, std_item, cutoff):
        """Implements the evaluation routine for the given evaluation type.
        
        Abstract method.
        """
        raise NotImplementedError('abstract')
    
    def set_fn(self, value):
        "Set the false negative counter after initialization."
        self.hits.fn = value
    
    def store_p_at_current_r(self):
        "Calculate and store current recall and precision."
        p = self.precision
        r = self.recall
        # self.logger.debug("P=%.5f @ current R=%.5f" % (p, r))
        self.precisions_at_recall[r].add(p)
    
    def yield_precision_recall_pairs(self):
        "Yield all (p, r) pairs sorted by ascending r, then descending p."
        for r in self._get_recall_values():
            precision_values = list(self.precisions_at_recall[r])
            precision_values.sort()
            precision_values.reverse()
            
            for p in precision_values:
                yield p, r
    
    def get_interpolated_pr_list(self):
        "Return a list of interpolated (precision, recall) values."
        recall_values = self._get_recall_values()
        interpolate = self._find_interpolation_points()
        interpolated_recall_values = [
            recall_values[pos]
            for pos, interpolated in enumerate(interpolate)
            if not interpolated
        ]
        interpolated_precision_values = [
            max(self.precisions_at_recall[r])
            for r in interpolated_recall_values
        ]
        return zip(interpolated_precision_values, interpolated_recall_values)
    
    @property
    def auc_ipr(self):
        """AUC iP/R score for the evaluation calculated from the order in
        which they were evaluated.
        """
        auc = 0.0
        last_r = 0.0
        
        for p, r in self.get_interpolated_pr_list():
            auc += p * (r - last_r)
            last_r = r
        
        return auc
    
    @property
    def p_at_full_r(self):
        "Maximum precision at full recall (or None)."
        try:
            return max(self.precisions_at_recall[1.0])
        except ValueError:
            del self.precisions_at_recall[1.0]
            return None
    
    @property
    def precision(self):
        hits = self.hits
        # self.logger.debug("precision from: tp=%i / (tp=%i + fp=%i)" % (
        #     hits.tp, hits.tp, hits.fp
        # ))
        return self._divide(hits.tp, float(hits.tp + hits.fp))
    
    @property
    def recall(self):
        hits = self.hits
        # self.logger.debug("recall from: tp=%i / (tp=%i + fn=%i)" % (
        #     hits.tp, hits.tp, hits.fn
        # ))
        return self._divide(hits.tp, float(hits.tp + hits.fn))
    
    def _get_recall_values(self):
        "Return all recall values sorted incrementally."
        recall_values = self.precisions_at_recall.keys()
        recall_values.sort()
        return recall_values
    
    def _find_interpolation_points(self):
        """Return a list of booleans for each recall value (in incremental
        order) where True denotes recall values that can be interpolated
        (i.e., removed).
        """
        recall_values = self._get_recall_values()
        recall_values.reverse()
        interpolate = [True] * len(recall_values)
        last_p = 0.0
        
        for pos, r in enumerate(recall_values):
            max_p = max(self.precisions_at_recall[r])
            
            if max_p > last_p:
                interpolate[pos] = False
                last_p = max_p
        
        interpolate.reverse()
        return interpolate
    
    @staticmethod
    def _divide(denominator, divisor):
        "Division result if divisor is not 0, otherwise return 0."
        if divisor == 0.0:
            return 0.0
        
        return denominator / divisor
    
