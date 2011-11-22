import logging

from collections import defaultdict
from math import sqrt

import biocreative.evaluation.calculation.hits as hits

class ProteinMacroEvaluation(dict):
    """Specialized list for the INT, IMT and IPT macro-averaged evaluations."""
    
    def __init__(self, *args, **kwds):
        super(ProteinMacroEvaluation, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("ProteinMacroEvaluation")
        self.precisions_at_recall = defaultdict(set)
    
    def std_dev(self, property_name):
        """Calculate the standard deviation for any of the properties."""
        assert property_name != 'avrg_p', 'AP cannot be averaged'
        
        if hasattr(self, property_name):
            sample = [getattr(data, property_name) for data in self.values()]
            return self._std_dev(sample)
        else:
            return 0.0
    
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
    
    def _get_recall_values(self):
        """Return all recall values sorted incrementally."""
        recall_values = self.precisions_at_recall.keys()
        recall_values.sort()
        return recall_values
    
    @property
    def recall(self):
        return self._average_for('recall')
    
    @property
    def precision(self):
        return self._average_for('precision')
    
    @property
    def f_score(self):
        return self._average_for('f_score')
    
    @property
    def avrg_p(self):
        """
        Average precision score for the evaluation calculated from the
        precision, recall values using a geometric curve approximation.
        """
        avrg_p = 0.0
        last_r = 0.0

        for p, r in self.yield_precision_recall_pairs():
            avrg_p += p * (r - last_r)
            last_r = r

        return avrg_p

    @property
    def hits(self):
        """Sum up all the hits in each individual (per document) result and
        return them in a Hit object.
        """
        hits_total = hits.Hits()
        hits_total.tp = sum(data.hits.tp for data in self.values())
        hits_total.fp = sum(data.hits.fp for data in self.values())
        hits_total.fn = sum(data.hits.fn for data in self.values())
        hits_total.tn = sum(data.hits.tn for data in self.values())
        return hits_total
    
    def _average_for(self, property_name):
        """Calculate the (macro-) average for a given property."""
        total = sum(getattr(data, property_name) for data in self.values())
        return total / len(self) if len(self) else 0.0
    
    @staticmethod
    def _std_dev(numbers):
        """Calculate the standard deviation of a list of numbers.
        sqrt(variance(numbers))
        """
        return sqrt(ProteinMacroEvaluation._variance(numbers))
    
    @staticmethod
    def _variance(numbers):
        """Measure the variance for a (small!) list of numbers.
        variation(numbers) / N
        """
        variation = ProteinMacroEvaluation._variation(numbers)
        return variation / float(len(numbers)) if len(numbers) else 0.0
    
    @staticmethod
    def _variation(numbers, avrg=None):
        """Measure the variation for a list of numbers.
        If avrg is not given, the mean is calculated, too, i.e.:
        sum( (i - avrg)^2 )
        With:
        avrg = mean(numbers) = sum(i) / N
        """
        if avrg is None:
            avrg = (
                sum(numbers) / float(len(numbers)) if len(numbers) else 0.0
            )
        
        return sum((x - avrg)**2 for x in numbers)
    
