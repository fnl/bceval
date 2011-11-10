from math import sqrt

from biocreative.evaluation.calculation.evaluation import AbstractEvaluation

class ArticleMccEvaluation(AbstractEvaluation):
    "Implementation for the ACT MCC and Accuracy evaluation."
    
    def evaluate(self, result_item, std_item, cutoff):
        """Count hits according to the classification in the results vs. the
        annotation in the GS.
        """
        assert type(result_item) is bool, \
            "Result item not a bool (is %s: %s)" % (
                result_item.__class__.__name__, str(result_item)
            )
        assert type(std_item) is bool, \
            "GS item not a bool (is %s: %s)" % (
                std_item.__class__.__name__, str(std_item)
            )
        attr = ''.join((
            't' if result_item == std_item else 'f',
            'p' if result_item is True else 'n'
        ))
        self.hits.add_to(attr, 1)
    
    @property
    def mcc_score(self):
        "Matthew's correlation coefficient."
        hits = self.hits
        self.logger.debug("mcc-score: tp=%i, tn=%i, fp=%i, fn=%i" % (
            hits.tp, hits.tn, hits.fp, hits.fp
        ))
        tpfp = hits.tp + hits.fp
        tpfn = hits.tp + hits.fn
        tnfp = hits.tn + hits.fp
        tnfn = hits.tn + hits.fn
        total = sqrt(tpfp * tpfn * tnfp * tnfn)
        tp_tn = hits.tp * hits.tn
        fp_fn = hits.fp * hits.fn
        return self._divide(tp_tn - fp_fn, total)
    
    @property
    def accuracy(self):
        hits = self.hits
        self.logger.debug("accuracy: tp=%i, tn=%i, fp=%i, fn=%i" % (
            hits.tp, hits.tn, hits.fp, hits.fp
        ))
        return self._divide(
            float(hits.tp + hits.tn), hits.sum()
        )
    
    @property
    def sensitivity(self):
        hits = self.hits
        self.logger.debug("sensitivity: tp=%i / (tp=%i + fn=%i)" % (
            hits.tp, hits.tp, hits.fn
        ))
        return self._divide(hits.tp, float(hits.tp + hits.fn))
    
    @property
    def specificity(self):
        hits = self.hits
        self.logger.debug("specificity: tn=%i / (tn=%i + fp=%i)" % (
            hits.tn, hits.tn, hits.fp
        ))
        return self._divide(hits.tn, float(hits.tn + hits.fp))
    
