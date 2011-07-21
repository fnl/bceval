import unittest

from mock import Mock, sentinel

from biocreative.evaluation.container.article_dict import ArticleDataDict

class ArticleDataDictTest(unittest.TestCase):
    
    def setUp(self):
        self.add = ArticleDataDict()
    
    def test_init_state(self):
        self.assertEqual(type(self.add.order), list)
        self.assertEqual(len(self.add.order), 0)
    
    def test_iterator(self):
        order = [sentinel._0, sentinel._1, sentinel._2]
        self.add.order = order
        
        for idx, item in enumerate(self.add):
            self.assertEqual(getattr(sentinel, "_%i" % idx), item)
    
    def test_keys(self):
        order = [sentinel._0, sentinel._1, sentinel._2]
        self.add.order = order
        self.assertEqual(order, self.add.keys())
    
    def test_assert_duplicates(self):
        # simply should not raise an assertion error
        self.add.assert_duplicates(sentinel.DOI, None)
    
    def test_assert_duplicates_raises_error(self):
        self.add[sentinel.DOI] = None
        self.assertRaises(
            AssertionError, self.add.assert_duplicates, sentinel.DOI, None
        )
    
    def test_add_result(self):
        self.add.add_result(sentinel.DOI, sentinel.ResultContainer)
        self.assertEqual(
            self.add.order, [sentinel.DOI], "order list not updated"
        )
        self.assertEqual(
            self.add.keys(), [sentinel.DOI], "incorrect dictionary keys"
        )
        self.assertEqual(
            self.add.values(), [sentinel.ResultContainer],
            "incorrect dictionary values"
        )
    
    def test_sort_result(self):
        self.add[1] = "b"
        self.add[2] = "c"
        self.add[3] = "a"
        self.add.sort_results()
        self.assertEqual(self.add.order, [3,1,2])
    
    def test_true_items(self):
        true_result_container = Mock()
        true_result_container.item = True
        false_result_container = Mock()
        false_result_container.item = False
        self.add[1] = false_result_container
        self.add[2] = true_result_container
        self.add[3] = false_result_container
        self.add[4] = true_result_container
        self.add[5] = false_result_container
        self.assertEqual(self.add.true_items(), 2)
    

if __name__ == '__main__':
    unittest.main()