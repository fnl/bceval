import unittest

from mock import Mock, patch

from biocreative.evaluation.calculation.article_auc_ipr \
    import ArticleAUCiPREvaluation
from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions

class ArticleAUCiPREvaluationTest(CalculationAssertions):
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def setUp(self, unused):
        self.evaluator = ArticleAUCiPREvaluation()
        self.evaluator.store_p_at_current_r = Mock()
        self.std_item = None
        
        for attr in C.HITS_ATTRIBUTES:
            setattr(self.evaluator.hits, attr, 2)
    
    def test_evaluate_with_true_item(self):
        self.evaluate_with_std_item(True)
        self.assert_hits(self.evaluator.hits, tp=3, tn=2, fp=2, fn=1)
    
    def test_evaluate_with_false_item(self):
        self.evaluate_with_std_item(False)
        self.assert_hits(self.evaluator.hits, tp=2, tn=2, fp=3, fn=2)
    
    def test_evaluate_with_illegal_item(self):
        self.assertRaises(TypeError, self.evaluator.evaluate, None, 1, None)
    
    def evaluate_with_std_item(self, flag):
        self.evaluator.evaluate(None, flag, None)
        self.assert_(self.evaluator.store_p_at_current_r.called)
    

if __name__ == '__main__':
    unittest.main()
