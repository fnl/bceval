import logging

from biocreative.evaluation.calculation import article_auc_pr, article_mcc

from biocreative.evaluation.controller.abstract import AbstractEvaluator

class ArticleEvaluator(AbstractEvaluator):
    """Implementation of the evaluation process for ACT."""
    
    def reset(self):
        """Reset the internal state to reuse the evaluator."""
        self.primary_eval = article_auc_pr.ArticleAucPrEvaluation()
        self.secondary_eval = article_mcc.ArticleMccEvaluation()
        self.results = None
        self.gold_standard = None
        self.logger = logging.getLogger("ArticleEvaluator")
    
    def _prepare(self):
        """Prepare the instance for the evaluation run."""
        self.primary_eval.hits.fn = self.gold_standard.true_items()
        self.secondary_eval.hits.fn = 0
        self.logger.info(
            "ACT evaluation fn=%i" % self.primary_eval.hits.fn
        )
    
    def _process(self):
        """Process all articles in the queue."""
        for doi in self.results.keys():
            if doi not in self.gold_standard:
                self.logger.error("ignoring unknown doi '%s'" % str(doi))
            else:
                self.logger.debug("processing article '%s'" % str(doi))
                self._process_doi(doi)
    
    def _process_doi(self, doi):
        """Evaluate the individual performance for the given article."""
        result_item = self.results[doi].item
        std_item = self.gold_standard[doi].item
        
        for this in (self.primary_eval, self.secondary_eval):
            this.evaluate(result_item, std_item, self.cutoff)
    
