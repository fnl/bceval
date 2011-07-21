import unittest

from collections import defaultdict
from mock import patch

from biocreative.evaluation.calculation.evaluation import AbstractEvaluation
from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions

class AbstractEvaluationTest(CalculationAssertions):
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def setUp(self, unused):
        self.evaluator = AbstractEvaluation()
        
        for attr in C.HITS_ATTRIBUTES:
            setattr(self.evaluator.hits, attr, 2)
        
        self.evaluator.hits.sum.return_value = 8
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def test_init_state(self, HitsMock):
        evaluator = AbstractEvaluation(doi="test", fn=0)
        self.assertTrue(HitsMock.called)
        HitsMock.assert_called_with(fn=0)
        self.assertEqual(evaluator.doi, "test")
        self.assert_(
            isinstance(evaluator.precisions_at_recall, defaultdict)
        )
    
    def test_set_fn(self):
        self.evaluator.set_fn(10)
        self.assertEqual(self.evaluator.hits.fn, 10)
    
    def test_pr_properties(self):
        for name in ("recall", "precision"):
            self.assert_property(name, 0.5)
    
    def set_up_ipr_test(self):
        for hits in (
            {'tp': 1, 'fp': 0, 'fn': 2, 'tn': 0}, # p=1.0, r=0.33
            {'tp': 1, 'fp': 1, 'fn': 2, 'tn': 0}, # p=0.5, r=0.33
            {'tp': 2, 'fp': 1, 'fn': 1, 'tn': 0}, # p=0.66, r=0.66
            {'tp': 2, 'fp': 2, 'fn': 1, 'tn': 0}, # p=0.5, r=0.66
            {'tp': 2, 'fp': 3, 'fn': 1, 'tn': 0}, # p=0.4, r=0.66
            {'tp': 3, 'fp': 3, 'fn': 0, 'tn': 0}, # p=0.5, r=1.0
        ):
            for attr, value in hits.items():
                setattr(self.evaluator.hits, attr, value)
            
            self.evaluator.store_p_at_current_r()
        
        self.p_at_full_r = 0.5
        self.ipr_values = [(1/1.0, 1/3.0), (2/3.0, 2/3.0), (3/6.0, 3/3.0)]
        self.pr_values = (
            (1/1.0, 1/3.0), (1/2.0, 1/3.0),
            (2/3.0, 2/3.0), (2/4.0, 2/3.0), (2/5.0, 2/3.0),
            (3/6.0, 3/3.0),
        )
        self.auc_ipr = 0.0
        last_r = 0.0
        
        for p, r in self.ipr_values:
            self.auc_ipr += p * (r - last_r)
            last_r = r
    
    def test_ipr_properties(self):
        self.set_up_ipr_test()
        self.assert_property("p_at_full_r", self.p_at_full_r)
        self.assert_property("auc_ipr", self.auc_ipr)
    
    def test_pr_values(self):
        self.set_up_ipr_test()
        ipr_values = self.evaluator.get_interpolated_pr_list()
        pr_values = tuple(self.evaluator.yield_precision_recall_pairs())
        self.assertEqual(pr_values, self.pr_values)
        self.assertEqual(ipr_values, self.ipr_values)
    

if __name__ == '__main__':
    unittest.main()
