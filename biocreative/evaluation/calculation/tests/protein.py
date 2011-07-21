import unittest

from mock import Mock, patch

from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions
from biocreative.evaluation.calculation.protein import ProteinEvaluation

class ProteinEvaluationTest(CalculationAssertions):
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def setUp(self, unused):
        self.evaluator = ProteinEvaluation()
        self.evaluator.store_p_at_current_r = Mock()
        
        for attr in C.HITS_ATTRIBUTES:
            setattr(self.evaluator.hits, attr, 2)
    
    def test_f_score(self):
        self.assert_property("f_score", 0.5)
    
    def test_evaluate_tp_item(self):
        self.evaluator.evaluate_item(1, [0,1,2])
        self.assert_hits(self.evaluator.hits, tp=3, fp=2, fn=1)
    
    def test_evaluate_fp_item(self):
        self.evaluator.evaluate_item(3, [0,1,2])
        self.assert_hits(self.evaluator.hits, tp=2, fp=3, fn=2)
    
    def test_evaluate_item_with_illegal_std_items(self):
        self.assertRaises(
            AssertionError, self.evaluator.evaluate_item, 1, (0,1,2)
        )
    
    def test_evaluate(self):
        self.evaluator.evaluate_item = Mock()
        gs_set = [0,1,2]
        self.evaluator.evaluate([3,4,1,2], gs_set, 3)
        self.assertTrue(self.evaluator.store_p_at_current_r.called)
        self.assertEqual(self.evaluator.store_p_at_current_r.call_count, 3)
        self.assertTrue(self.evaluator.evaluate_item.called)
        self.assertEqual(self.evaluator.evaluate_item.call_count, 3)
        arg_list = self.evaluator.evaluate_item.call_args_list
        exp_list = (((3, gs_set), {}), ((4, gs_set), {}), ((1, gs_set), {}))
        
        for call, args in enumerate(arg_list):
            self.assert_values(
                "evaluate_item call %i" % (call + 1), exp_list[call], args
            )
    
    def test_evaluate_with_illegal_result_items(self):
        self.assertRaises(
            AssertionError, self.evaluator.evaluate, (1,2,3), set([0,1,2]), 2
        )
    

if __name__ == '__main__':
    unittest.main()