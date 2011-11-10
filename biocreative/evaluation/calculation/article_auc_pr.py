from biocreative.evaluation.calculation.evaluation import AbstractEvaluation

class ArticleAucPrEvaluation(AbstractEvaluation):
    """Implementation for the ACT AUC P/R evaluation.
    
    I.e., only looks at the annotation in the GS to determine if this
    classification should be counted as FP or TP. This is good enough to
    calculate the AUC iP/R score. However, it cannot be uses to
    calculate the MCC score and Accuracy!
    """
    
    def evaluate(self, result_item, std_item, cutoff):
        """If the article is positive (True) in the GS, increase tp count and
        decrease fn count, otherwise increase fp count.
        
        Arguments are:
        result_item (not used here), gs_item, cutoff (not used here)
        """
        if std_item is True:
            self.hits.tp += 1
            self.hits.fn -= 1
        elif std_item is False:
            self.hits.fp += 1
        else:
            raise TypeError("GS item not a bool (is %s: %s)" % (
                std_item.__class__.__name__, str(std_item)
            ))
        
        self.store_p_at_current_r()
    
    @property
    def auc_pr(self):
        """AUC P/R score using the exact precision, recall curve."""
        auc = 0.0
        last_r = 0.0
        last_p = 1.0

        for p, r in self.yield_precision_recall_pairs():
            auc += (p + last_p) / 2 * (r - last_r)
            last_r = r
            last_p = p

        return auc
    
