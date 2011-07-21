import unittest

from random import shuffle

from biocreative.evaluation.container.results import ResultContainer

class ResultContainerTest(unittest.TestCase):
    
    def test_init_state(self):
        self.init_state_test_helper(True, rank=1, confidence=1.0)
        self.init_state_test_helper(False)
        self.init_state_test_helper("P12345", confidence=1.0)
        self.init_state_test_helper(("P12345", "Q12345"), rank=1)
    
    def init_state_test_helper(self, item, rank=None, confidence=None):
        rc = ResultContainer(item, rank=rank, confidence=confidence)
        self.assertEqual(rc.item, item)
        self.assertEqual(rc.rank, rank)
        self.assertEqual(rc.confidence, confidence)
        self.assertEqual(rc._boolean, isinstance(item, bool))
        ordering = -1 if (isinstance(item, bool) and item is False) else 1
        self.assertEqual(rc._ordering, ordering)
    
    def test_len(self):
        self.assertEqual(len(ResultContainer((1,2), rank=3)), 1)
    
    def test_str(self):
        rc_str = str(ResultContainer(True, rank=1, confidence=0.5))
        self.assertEqual(rc_str, "True\t1\t%f" % 0.5)
    
    def test_repr(self):
        rc_str = repr(ResultContainer(("A", "B"), rank=1, confidence=0.5))
        self.assertEqual(rc_str, "<ResultContainer 'A B 1 %f'>" % 0.5)
    
    def test_illegal_comparison_raises_type_error(self):
        rc_bool = ResultContainer(True, rank=1)
        rc_str = ResultContainer("A", rank=2)
        rc_list = [rc_bool, rc_str]
        self.assertRaises(TypeError, rc_list.sort)
    
    def test_order_boolean_items_by_rank(self):
        rc1 = ResultContainer(True, rank=1)
        rc2 = ResultContainer(True, rank=3)
        rc3 = ResultContainer(False, rank=4)
        rc4 = ResultContainer(False, rank=2)
        self.order_test_helper([rc1, rc2, rc3, rc4])
    
    def test_order_boolean_items_by_confidence(self):
        rc1 = ResultContainer(True,  confidence=1.0)
        rc2 = ResultContainer(True,  confidence=0.5)
        rc3 = ResultContainer(False, confidence=0.5)
        rc4 = ResultContainer(False, confidence=1.0)
        self.order_test_helper([rc1, rc2, rc3, rc4])
    
    def test_order_boolean_items_by_rank_and_confidence(self):
        rc1 = ResultContainer(True, rank=1, confidence=0.5)
        rc2 = ResultContainer(True, rank=3, confidence=1.0)
        rc3 = ResultContainer(False, rank=4, confidence=0.5)
        rc4 = ResultContainer(False, rank=2, confidence=1.0)
        self.order_test_helper([rc1, rc2, rc3, rc4])
    
    def test_order_string_items(self):
        self.order_test_helper_for_non_bolean_items("A", "B", "C", "D")
    
    def test_order_tuple_items(self):
        self.order_test_helper_for_non_bolean_items(
            (1, "A"), (2, "B"), (3, "C"), (4, "D")
        )
    
    def order_test_helper_for_non_bolean_items(self, A, B, C, D):
        self.order_test_helper_for_raw_items(          [A, B, C, D])
        self.order_test_helper_for_rank(               [C, B, A, D])
        self.order_test_helper_for_confidence(         [B, C, A, D])
        self.order_test_helper_for_rank_and_confidence([C, B, A, D])
    
    def order_test_helper_for_raw_items(self, items):
        result_list = [
            ResultContainer(items[0]),
            ResultContainer(items[1]),
            ResultContainer(items[2]),
            ResultContainer(items[3])
        ]
        self.order_test_helper(result_list)
    
    def order_test_helper_for_rank(self, items):
        result_list = [
            ResultContainer(items[0], rank=1),
            ResultContainer(items[1], rank=2),
            ResultContainer(items[2], rank=3),
            ResultContainer(items[3], rank=4)
        ]
        self.order_test_helper(result_list)
    
    def order_test_helper_for_confidence(self, items):
        result_list = [
            ResultContainer(items[0], confidence=1.0),
            ResultContainer(items[1], confidence=1.0),
            ResultContainer(items[2], confidence=0.5),
            ResultContainer(items[3], confidence=0.5)
        ]
        self.order_test_helper(result_list)
    
    def order_test_helper_for_rank_and_confidence(self, items):
        result_list = [
            ResultContainer(items[0], rank=1, confidence=1.0),
            ResultContainer(items[1], rank=2, confidence=1.0),
            ResultContainer(items[2], rank=3, confidence=0.5),
            ResultContainer(items[3], rank=4, confidence=0.5)
        ]
        self.order_test_helper(result_list)
    
    def order_test_helper(self, expected):
        result = list(expected)
        
        for i in range(10):
            shuffle(result)
            result.sort()
            self.assertEqual(expected, result)
    

if __name__ == '__main__':
    unittest.main()