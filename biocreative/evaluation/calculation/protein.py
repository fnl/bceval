from biocreative.evaluation.calculation.evaluation import AbstractEvaluation

class ProteinEvaluation(AbstractEvaluation):
    "Implementation for the INT and IPT evaluations providing F-score."
    
    def evaluate(self, result_list, std_set, cutoff):
        """Iterate over a list of results for a document, comparing them to
        a set of GS items.
        
        If cutoff is > 0, break when reaching that rank order.
        """
        assert isinstance(result_list, list), \
            "Result items not a list (is %s)" \
            % result_list.__class__.__name__
        
        for rank, item in enumerate(result_list):
            self.evaluate_item(item, std_set)
            self.store_p_at_current_r()
            
            if rank + 1 == cutoff:
                break
    
    def evaluate_item(self, result_item, std_set):
        """If the classification is in the GS set, increase TP and decrease
        FN, otherwise increase FP.
        """
        assert isinstance(std_set, list), \
            "GS items not a list (is %s)" % std_set.__class__.__name__
        
        if result_item in std_set:
            self.hits.tp += 1
            self.hits.fn -= 1
        else:
            self.hits.fp += 1
    
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
    def f_score(self):
        "Balanced (beta=1.0) F-measure for the Hit set."
        p = self.precision
        r = self.recall
        # self.logger.debug("f-score from: p=%.5f, r=%.5f" % (p, r))
        return self._divide(2.0 * p * r, p + r)
    
