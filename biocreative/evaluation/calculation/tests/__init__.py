import unittest

from math import sqrt
from random import randint, sample

from biocreative.evaluation.calculation.article_auc_pr \
    import ArticleAucPrEvaluation
from biocreative.evaluation.calculation.article_mcc \
    import ArticleMccEvaluation
from biocreative.evaluation.calculation.protein_evaluation \
    import ProteinEvaluation
from biocreative.evaluation.calculation.macro_evaluation \
    import ProteinMacroEvaluation
from biocreative.evaluation.calculation.tests.test_helpers \
    import CalculationAssertions

class CalculationTests(CalculationAssertions):
    
    def test_article_auc_pr(self):
        self.evaluator = CalculationTests.simulate_article_evaluator(
            ArticleAucPrEvaluation, 3
        )
        self.assert_hits(self.evaluator.hits, tp=3, fp=7, fn=0, tn=0)
        self.assert_property("p_at_full_r", 3/8.0)
        recall_span = 1/3.0
        self.assert_property(
            "auc_pr",
            (1/1.0 + 1/1.0)/2 * recall_span +
            (1/4.0 + 2/5.0)/2 * recall_span +
            (2/7.0 + 3/8.0)/2 * recall_span
        )
    
    def test_article_mcc(self):
        self.evaluator = CalculationTests.simulate_article_evaluator(
            ArticleMccEvaluation, 0
        )
        self.assert_hits(self.evaluator.hits, tp=2, fp=2, fn=1, tn=5)
        self.assert_property("sensitivity", 2/3.0) # tp / (tp + fn)
        self.assert_property("specificity", 5/7.0) # tn / (tn + fp)
        self.assert_property("accuracy", 7/10.0) # (tp + tn) / sum(hits)
        self.assert_property(
            "mcc_score", (2*5 - 2*1) / sqrt(4*3*7*6)
        ) # (tp*tn - fp*fn) / sqrt(tp+fp * tp+fn * tn+fp * tn+fn)
    
    @staticmethod
    def simulate_article_evaluator(EvaluatorClass, fn_count):
        evaluator = EvaluatorClass(fn=fn_count)
        t = True
        f = False
        
        for result_item, std_item in [
            (t, t), (f, f), (f, f), (t, f), (f, t),
            (f, f), (f, f), (t, t), (f, f), (t, f)
        ]:
            evaluator.evaluate(result_item, std_item, None)
        
        return evaluator
    
    def test_protein_for_normalizations(self):
        self.helper_protein(["A", "B", "C", "D"], ["A", "C", "D"])
    
    def test_protein_for_pairs(self):
        A, B, C, D = ("a", "x"), ("b", "y"), ("c", "z"), ("d", "w")
        self.helper_protein([A, B, C, D], [A, C, D])
    
    def helper_protein(self, result_items, std_items):
        self.evaluator = ProteinEvaluation(doi="test", fn=3)
        self.evaluator.evaluate(result_items, std_items, 3)
        self.assert_hits(self.evaluator.hits, tp=2, fp=1, fn=1, tn=0)
        p = 2/3.0
        r = 2/3.0
        self.assert_property("precision", p)
        self.assert_property("recall", r)
        self.assert_property("f_score", 2.0 * p * r / (p + r))
        self.assert_property("p_at_full_r", None)
        self.assert_property("avrg_p", 1/1.0 * 1/3.0 + 2/3.0 * 1/3.0)
    
    def test_macro_evaluation(self):
        protein_results = [
            CalculationTests.random_protein_result() for i in range(50)
        ]
        self.evaluator = ProteinMacroEvaluation(
            ((i, r) for i, r in enumerate(protein_results))
        )
        N = len(protein_results)
        precision = sum(p.precision for p in protein_results) / N
        recall = sum(p.recall for p in protein_results) / N
        f_score = sum(p.f_score for p in protein_results) / N
        self.assert_property("precision", precision)
        self.assert_property("recall", recall)
        self.assert_property("f_score", f_score)
    
    @staticmethod
    def random_protein_result():
        results = list(set([randint(1, 100) for i in range(100)]))
        gold_standard = sample(range(1, 101), 10)
        evaluator = ProteinEvaluation(doi="test", fn=len(gold_standard))
        evaluator.evaluate(results, gold_standard, 0)
        return evaluator
    

def calculation_modules():
    module_path = 'biocreative.evaluation.calculation.tests'
    module_names = [
        'article_auc_pr',
        'article_mcc',
        'evaluation',
        'hits',
        'macro_evaluation',
        'protein'
    ]
    yield module_path
    
    for module in module_names:
        print "%s.%s" % (module_path, module)
        yield "%s.%s" % (module_path, module)

if __name__ == '__main__':
    unittest.main()