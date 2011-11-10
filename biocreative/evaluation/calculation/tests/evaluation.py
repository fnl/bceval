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
    

if __name__ == '__main__':
    unittest.main()
