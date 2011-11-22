import unittest

from mock import Mock, patch

from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions
from biocreative.evaluation.calculation.protein_evaluation import ProteinEvaluation

class ProteinEvaluationTest(CalculationAssertions):
    
    @patch('biocreative.evaluation.calculation.hits.Hits', spec=True)
    def setUp(self, unused):
        self.evaluator = ProteinEvaluation()
        
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
        self.evaluator.store_p_at_current_r = Mock()
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
    
    def set_up_avrg_p_test(self):
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
        self.avrg_p_values = [(1/1.0, 1/3.0), (2/3.0, 2/3.0), (3/6.0, 3/3.0)]
        self.pr_values = (
            (1/1.0, 1/3.0), (1/2.0, 1/3.0),
            (2/3.0, 2/3.0), (2/5.0, 2/3.0),
            (3/6.0, 3/3.0),
        )
        self.avrg_p = 0.0
        last_r = 0.0
        
        for p, r in self.avrg_p_values:
            self.avrg_p += p * (r - last_r)
            last_r = r
    
    def test_avrg_p_properties(self):
        self.set_up_avrg_p_test()
        self.assert_property("p_at_full_r", self.p_at_full_r)
        self.assert_property("avrg_p", self.avrg_p)
    
    def test_pr_values(self):
        self.set_up_avrg_p_test()
        pr_values = tuple(self.evaluator.yield_precision_recall_pairs())
        self.assertEqual(pr_values, self.pr_values)


if __name__ == '__main__':
    unittest.main()