import logging

from math import sqrt

import biocreative.evaluation.calculation.hits as hits

class ProteinMacroEvaluation(list):
    "Specialized list for the INT and IPT macro-averaged evaluations."
    
    def __init__(self, *args, **kwds):
        super(ProteinMacroEvaluation, self).__init__(*args, **kwds)
        self.logger = logging.getLogger("ProteinMacroEvaluation")
    
    def std_dev(self, property_name):
        "Calculate the standard deviation for any of the properties."
        if hasattr(self, property_name):
            sample = [getattr(data, property_name) for data in self]
            return self._std_dev(sample)
        else:
            return 0.0
    
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
    def auc_ipr(self):
        return self._average_for('auc_ipr')
    
    @property
    def hits(self):
        """Sum up all the hits in each individual (per document) result and
        return them in a Hit object.
        """
        hits_total = hits.Hits()
        hits_total.tp = sum(data.hits.tp for data in self)
        hits_total.fp = sum(data.hits.fp for data in self)
        hits_total.fn = sum(data.hits.fn for data in self)
        hits_total.tn = sum(data.hits.tn for data in self)
        return hits_total
    
    def _average_for(self, property_name):
        "Calculate the (macro-) average for a given property."
        total = sum(getattr(data, property_name) for data in self)
        return (total / len(self) if len(self) else 0.0)
    
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
        return (variation / float(len(numbers)) if len(numbers) else 0.0)
    
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
    
