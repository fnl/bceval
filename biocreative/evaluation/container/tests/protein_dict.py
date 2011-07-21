import unittest

from mock import Mock, sentinel

from biocreative.evaluation.container.protein_dict import ProteinDataDict

class ProteinDataDictTest(unittest.TestCase):
    def setUp(self):
        self.pdd = ProteinDataDict()
    
    def test_assert_duplicates(self):
        result_container_mock = Mock()
        result_container_mock.item = sentinel.Item
        self.pdd[sentinel.DOI] = [result_container_mock]
        self.pdd.assert_duplicates(sentinel.DOI, sentinel.OtherItem)
        
        self.assert_sentinel_DOI_is_the_only_key()
        self.assert_sentinel_DOI_value_is([result_container_mock])
    
    def test_assert_duplicates_raises_error(self):
        result_container_mock = Mock()
        result_container_mock.item = sentinel.Item
        self.pdd[sentinel.DOI] = [result_container_mock]
        
        self.assertRaises(
            AssertionError, self.pdd.assert_duplicates,
            sentinel.DOI, sentinel.Item
        )
    
    def test_assert_duplicates_creates_list(self):
        self.pdd.assert_duplicates(sentinel.DOI, sentinel.ResultContainer)
        
        self.assert_sentinel_DOI_is_the_only_key()
        self.assert_sentinel_DOI_value_is([])
    
    def test_add_result(self):
        self.pdd[sentinel.DOI] = list()
        self.pdd.add_result(sentinel.DOI, sentinel.ResultContainer)
        
        self.assert_sentinel_DOI_is_the_only_key()
        self.assert_sentinel_DOI_value_is([sentinel.ResultContainer])
    
    def test_sort_results(self):
        self.pdd[sentinel.DOI] = [3,2,1,4]
        self.pdd.sort_results()
        
        self.assert_sentinel_DOI_is_the_only_key()
        self.assert_sentinel_DOI_value_is([1,2,3,4])
    
    def test_true_items(self):
        self.pdd[1] = [None] * 3
        self.pdd[2] = [None] * 2
        self.pdd[3] = [None] * 1
        self.pdd[4] = [None] * 0
        self.pdd[5] = [None] * 5
        self.assertEqual(self.pdd.true_items(), 11)
    
    def assert_sentinel_DOI_is_the_only_key(self):
        self.assertEqual([sentinel.DOI], self.pdd.keys())
    
    def assert_sentinel_DOI_value_is(self, expectation):
        self.assertEqual(expectation, self.pdd[sentinel.DOI])
    

if __name__ == '__main__':
    unittest.main()