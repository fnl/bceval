import logging

from biocreative.evaluation.calculation.macro_evaluation import \
    ProteinMacroEvaluation
from biocreative.evaluation.calculation.protein_evaluation import \
    ProteinEvaluation
from biocreative.evaluation.controller.abstract import AbstractEvaluator

class ProteinEvaluator(AbstractEvaluator):
    "Implementation of the evaluation process for INT and IPT."
    
    def reset(self):
        "Reset the internal state to reuse the evaluator."
        self.primary_eval = ProteinEvaluation()
        self.secondary_eval = ProteinMacroEvaluation()
        self.results = None
        self.gold_standard = None
        self.logger = logging.getLogger("ProteinEvaluator")
    
    def _prepare(self, results, gold_standard):
        "Prepare the instance for the evaluation run."
        assert len(results) == len(gold_standard), \
            "the entries in the evaluation result and the gold standard " \
            "do not match"
        
        self.primary_eval.set_fn(gold_standard.true_items())
        self.logger.debug(
            "INT/IPT evaluation: %i GS annotations" % 
            self.primary_eval.hits.fn
        )
    
    def _process(self):
        "Process the result set."
        self._dois = self.results.keys()
        self._dois.sort()
        result_sizes = [
            len(result_list) for result_list in self.results.values()
        ]
        max_rank_in_results = max(result_sizes) if len(result_sizes) else 0
        self.logger.info("longest result set has %i annotations",
                         max_rank_in_results)
        
        if self.cutoff and self.cutoff < max_rank_in_results:
            max_rank_in_results = self.cutoff
        
        for doi in list(self._dois):
            result_items = self.results[doi]
            std_items = self.gold_standard[doi]
            result_doc = ProteinEvaluation(doi=doi, fn=len(std_items))
            self.secondary_eval[doi] = result_doc
            
        for rank in range(max_rank_in_results):
            for doi in list(self._dois):
                self._process_doi(doi, rank)
            
            # Calculate & store the average P/R pair
            # at this rank over all documents (macro-averaging)
            self.secondary_eval.store_p_at_current_r()
            # Calculate & store the current P/R value
            # at this rank over all documents (micro-averaging)
            self.primary_eval.store_p_at_current_r()
    
    def _process_doi(self, doi, rank):
        "Evaluate the result at a given rank for a document."
        result_items = self.results[doi]
        std_items = self.gold_standard.get(doi) # special syntax for mocking
        
        try:
            item = result_items[rank]
        except IndexError:
            # no more results for this DOI
            self._dois.remove(doi)
        else:
            # evaluate the result at the current rank
            self.primary_eval.evaluate_item(item, std_items)
            self.secondary_eval[doi].evaluate_item(item, std_items)
