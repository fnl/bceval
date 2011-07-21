import unittest

from biocreative.evaluation.calculation.hits import Hits
from biocreative.evaluation.calculation.tests.test_helpers \
    import Constants as C, CalculationAssertions

class HitsTest(CalculationAssertions):
    
    def setUp(self):
        self.hits = Hits()
    
    def test_init_state(self):
        self.assert_counter(self.hits, tp=0, fp=0, tn=0, fn=None)
    
    def test_setters(self):
        for name in C.HITS_ATTRIBUTES:
            self.assert_setting_property(name, 1)
    
    def test_getters(self):
        self.assert_hits(self.hits, tp=0, fp=0, tn=0, fn=None)
    
    def test_setting_illegal_values(self):
        for name, value in (
            ("tp", -1), ("fp", 1.0), ("tn", "bad"), ("fn", None)
        ):
            self.assert_setting_illegal_property(name, value)
    
    def test_add_to_method(self):
        current = self.hits.tp
        increment = 5
        self.hits.add_to("tp", increment)
        self.assert_counter(self.hits, tp=current + increment)
    
    def test_add_to_method_with_illegal_values(self):
        self.assertRaises(AssertionError, self.hits.add_to, "tp", -1)
        self.assertRaises(AssertionError, self.hits.add_to, "fp", 1.0)
        self.assertRaises(TypeError, self.hits.add_to, "tn", "bad")
        self.assertRaises(TypeError, self.hits.add_to, "tn", None)
        self.assertRaises(AttributeError, self.hits.add_to, "bad", 1)
    
    def set_up_for_sum_and_all(self):
        test = { 'tp': 0, 'fp': 1, 'fn': 2, 'tn': 3 }
        self.expected_items = test.values()
        self.checksum = sum(self.expected_items)
        
        for key, value in test.items():
            setattr(self.hits, key, value)
    
    def test_sum(self):
        self.set_up_for_sum_and_all()
        testsum = self.hits.sum()
        self.assertEqual(
            self.checksum, testsum, "iterator checksum failed (%i)" % testsum
        )
    
    def test_all(self):
        self.set_up_for_sum_and_all()
        items = self.hits.all()
        
        for i in items:
            self.assertTrue(
                i in self.expected_items,
                "value '%s' should not be returned by the iterator" % str(i)
            )
            self.expected_items.remove(i)
        
        self.assertEqual(
            0, len(self.expected_items),
            "not all iterator items found; missing %s" % str(
                self.expected_items
            )
        )
    
    def assert_setting_property(self, name, to_value):
        setattr(self.hits, name, to_value)
        self.assert_counter(self.hits, **{name: to_value})
    
    def assert_setting_illegal_property(self, name, to_value):
        self.assertRaises(AssertionError, setattr, self.hits, name, to_value)
    

if __name__ == '__main__':
    unittest.main()
