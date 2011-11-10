import unittest

from math import sqrt
from mock import patch

from biocreative.evaluation.calculation.article_mcc \
    import ArticleMccEvaluation
from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions

class ArticleMccEvaluationTest(CalculationAssertions):
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def setUp(self, unused):
        self.evaluator = ArticleMccEvaluation()
        
        for attr in C.HITS_ATTRIBUTES:
            setattr(self.evaluator.hits, attr, 2)
        
        self.evaluator.hits.sum.return_value = 8
    
    def test_properties(self):
        for name in ("specificity", "sensitivity"):
            self.assert_property(name, 0.5)
        
        self.assertFalse(self.evaluator.hits.sum.called)
        self.assert_property("accuracy", 0.5)
        self.assertTrue(self.evaluator.hits.sum.called) # by accuracy
        self.evaluator.hits.tp += 1 # so MCC doesn't produce 0
        self.assert_property("mcc_score", 2.0 / sqrt(5*5*4*4))
    
    def test_evaluate_with_tp_item(self):
        self.evaluate_with(True, True, 'tp')
    
    def test_evaluate_with_fp_item(self):
        self.evaluate_with(True, False, 'fp')
    
    def test_evaluate_with_fn_item(self):
        self.evaluate_with(False, True, 'fn')
    
    def test_evaluate_with_tn_item(self):
        self.evaluate_with(False, False, 'tn')
    
    def test_evaluate_with_illegal_result_item_raises_assertion_error(self):
        self.assertRaises(
            AssertionError, self.evaluator.evaluate, 1, True, None
        )
    
    def test_evaluate_with_illegal_std_item_raises_assertion_error(self):
        self.assertRaises(
            AssertionError, self.evaluator.evaluate, True, 1, None
        )
    
    def evaluate_with(self, result, std, attr):
        self.evaluator.evaluate(result, std, None)
        self.evaluator.hits.add_to.assert_called_with(attr, 1)
    

if __name__ == '__main__':
    unittest.main()
