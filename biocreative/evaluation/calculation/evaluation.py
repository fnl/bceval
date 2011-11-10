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
        """Set the false negative counter after initialization."""
        self.hits.fn = value
    
    def store_p_at_current_r(self):
        """Calculate and store current recall and precision."""
        self.precisions_at_recall[self.recall].add(self.precision)
    
    def yield_precision_recall_pairs(self):
        """Yield all (p, r) pairs sorted by ascending r, then descending p."""
        for r in self._get_recall_values():
            precision_values = list(self.precisions_at_recall[r])
            
            if len(precision_values) > 1:
                precision_values.sort()
                yield precision_values[-1], r
            
            yield precision_values[0], r
    
    @property
    def p_at_full_r(self):
        """Maximum precision at full recall (or None)."""
        try:
            return max(self.precisions_at_recall[1.0])
        except ValueError:
            del self.precisions_at_recall[1.0]
            return None
    
    @property
    def precision(self):
        "Precision evaluation."
        hits = self.hits
        # self.logger.debug("precision from: tp=%i / (tp=%i + fp=%i)" % (
        #     hits.tp, hits.tp, hits.fp
        # ))
        return self._divide(hits.tp, float(hits.tp + hits.fp))
    
    @property
    def recall(self):
        "Recall evaluation."
        hits = self.hits
        # self.logger.debug("recall from: tp=%i / (tp=%i + fn=%i)" % (
        #     hits.tp, hits.tp, hits.fn
        # ))
        return self._divide(hits.tp, float(hits.tp + hits.fn))
    
    def _get_recall_values(self):
        """Return all recall values sorted incrementally."""
        recall_values = self.precisions_at_recall.keys()
        recall_values.sort()
        return recall_values
    
    @staticmethod
    def _divide(denominator, divisor):
        """Division result if divisor is not 0, otherwise return 0."""
        if divisor == 0.0:
            return 0.0
        
        return denominator / divisor
    
