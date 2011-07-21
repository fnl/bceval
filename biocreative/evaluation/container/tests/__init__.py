import unittest

from random import shuffle
from mock import sentinel as s

from biocreative.evaluation.container.article_dict import ArticleDataDict
from biocreative.evaluation.container.protein_dict import ProteinDataDict
from biocreative.evaluation.container.results import ResultContainer

class ContainerTests(unittest.TestCase):
    
    def setUp(self):
        self.article_data = [
            (s.DOI1, True, 1, 1.0),
            (s.DOI2, False, 1, 0.8),
            (s.DOI3, True, 2, 0.6),
            (s.DOI4, False, 2, 0.4),
            (s.DOI5, True, 3, 0.2)
        ]
        self.protein_data = [
            (s.DOI1, s.Data1, 1, 1.0),
            (s.DOI1, s.Data2, 2, 0.5),
            (s.DOI2, s.Data3, 1, 1.0),
            (s.DOI2, s.Data4, 2, 0.8),
            (s.DOI2, s.Data5, 3, 0.6)
        ]
    
    # ===================
    # = ArticleDataDict =
    # ===================
    
    def test_article_data_dict(self):
        for i in range(10):
            self.article_data_dict_test_helper()
    
    def article_data_dict_test_helper(self):
        add = ArticleDataDict()
        add.load_from(self.article_data_iterator())
        self.compare_keys([s.DOI1, s.DOI3, s.DOI5, s.DOI4, s.DOI2], add)
        
        for key, expected_rc in self.article_data_dict().items():
            received_rc = add[key]
            self.compare_result_container_content(
                expected_rc, received_rc
            )
        
        self.assertEqual(add.true_items(), 3)
    
    def test_article_loading_of_duplicate_data_raises_error(self):
        self.article_data.append((s.DOI1, False, 3, 0.2))
        add = ArticleDataDict()
        self.assertRaises(
            AssertionError, add.load_from, self.article_data_iterator()
        )
    
    def test_article_loading_of_duplicate_ranks_raises_error(self):
        self.article_data.append((s.DOI6, False, 2, 0.2))
        add = ArticleDataDict()
        self.assertRaises(
            RuntimeError, add.load_from, self.article_data_iterator()
        )
    
    # ===================
    # = ProteinDataDict =
    # ===================
    
    def test_protein_data_dict(self):
        for i in range(10):
            self.protein_data_dict_test_helper()
    
    def protein_data_dict_test_helper(self):
        pdd = ProteinDataDict()
        pdd.load_from(self.protein_data_iterator())
        test_iter = iter(pdd)
        expected_pdd = ContainerTests.protein_data_dict()
        self.compare_keys([s.DOI1, s.DOI2], pdd)
        
        for doi in [s.DOI1, s.DOI2]:
            next_doi = test_iter.next()
            self.assertEqual(doi, next_doi)
            self.assertEqual(len(pdd[doi]), len(expected_pdd[doi]))
            
            for idx, expected_rc in enumerate(expected_pdd[doi]):
                received_rc = pdd[doi][idx]
                self.compare_result_container_content(
                    expected_rc, received_rc
                )
        
        self.assertEqual(pdd.true_items(), 5)
    
    def test_protein_loading_of_duplicate_data_raises_error(self):
        self.protein_data.append((s.DOI2, s.Data4, 4, 0.4))
        pdd = ProteinDataDict()
        self.assertRaises(
            AssertionError, pdd.load_from, self.protein_data_iterator()
        )
    
    def test_protein_loading_of_duplicate_ranks_raises_error(self):
        self.protein_data.append((s.DOI1, s.Data6, 2, 0.4))
        pdd = ProteinDataDict()
        self.assertRaises(
            RuntimeError, pdd.load_from, self.protein_data_iterator()
        )
    
    # ===========
    # = Helpers =
    # ===========
    
    def compare_keys(self, expected, dd):
        self.assertEqual(len(dd), len(expected))
        self.assertEqual(dd.keys(), expected)
    
    def compare_result_container_content(self, expected_rc, received_rc):
        self.assertEqual(received_rc.item, expected_rc.item)
        self.assertEqual(received_rc.rank, expected_rc.rank)
        self.assertEqual(received_rc.confidence, expected_rc.confidence)
    
    def article_data_iterator(self):
        return ContainerTests.data_iterator(self.article_data)
    
    def protein_data_iterator(self):
        return ContainerTests.data_iterator(self.protein_data)
    
    @staticmethod
    def data_iterator(data):
        shuffle(data)
        return iter(data)
    
    def article_data_dict(self):
        add = dict()
        
        for doi, flag, rank, conf in self.article_data:
            add[doi] = ResultContainer(flag, rank=rank, confidence=conf)
        
        return add
    
    @staticmethod
    def protein_data_dict():
        return {
            s.DOI1: [
                ResultContainer(s.Data1, 1, 1.0),
                ResultContainer(s.Data2, 2, 0.5)
            ],
            s.DOI2: [
                ResultContainer(s.Data3, 1, 1.0),
                ResultContainer(s.Data4, 2, 0.8),
                ResultContainer(s.Data5, 3, 0.6)
            ]
        }

if __name__ == '__main__':
    unittest.main()