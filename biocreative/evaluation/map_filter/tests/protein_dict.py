import unittest

from mock import Mock, sentinel

from biocreative.evaluation.container.results import ResultContainer
from biocreative.evaluation.map_filter.protein_dict \
    import AbstractProteinDataDict

class AbstractProteinDataDictTest(unittest.TestCase):
    
    def setUp(self):
        self.data = AbstractProteinDataDict()
    
    def test_init_state(self):
        pass
    
    def test_map_homonym_orthologs(self):
        self.data._mapping_setup = Mock()
        self.data.extract_accessions_for = Mock()
        self.data._add_ho_gs_mappings_for = Mock()
        self.data._map = Mock()
        self.data._mapping_logging_and_assertions = Mock()
        rc1 = Mock(spec=ResultContainer)
        rc1.item = 'a'
        rc2 = Mock(spec=ResultContainer)
        rc2.item = 'b'
        gs = { 1: [rc1, rc2], 2: None, 3: None }
        self.data[1] = [rc1, rc2]
        self.data[2] = []
        self.data.map_homonym_orthologs(sentinel.ho_map, gs)
        self.assert_called_once(self.data._mapping_setup, sentinel.ho_map)
        self.assert_called_once(self.data._mapping_logging_and_assertions)
        self.assert_called_once(self.data._map, 1)
        self.assert_called_once(self.data.extract_accessions_for, 1)
        self.assert_called_with(
            self.data._add_ho_gs_mappings_for, [(('a',), {}), (('b',), {})]
        )
    
    def test_mapping_setup(self):
        self.data.update( { 1: ['a', 'b'], 2: ['c'], 3: [], 4: ['d'] } )
        self.data._mapping_setup(sentinel.ho_map)
        self.assertEqual(self.data._ho_map, sentinel.ho_map)
        self.assertEqual(self.data._mapped_results, 0)
        self.assertEqual(self.data._added_results, 0)
        self.assertEqual(self.data._filtered_results, 0)
        self.assertEqual(self.data._ho_gs_lists, None)
        self.assertEqual(self.data._result_accessions, None)
        self.assertEqual(self.data._result_container, None)
        self.assertEqual(self.data._replaced_an_entry, False)
        self.assertEqual(self.data._old_results_size, 4)
    
    def test_add_ho_gs_mappings_for(self):
        self.data._item_in_ho_map = Mock()
        self.data._item_in_ho_map.return_value = True
        self.data._item_iterator = Mock()
        self.data._item_iterator.return_value = [1, 2, 3]
        self.data._ho_gs_lists = { 1: [], 2: [], 3: [] }
        self.data._gs_items = [1]
        self.data._add_ho_gs_mappings_for('a')
        self.assert_called_once(self.data._item_in_ho_map, 'a')
        self.assert_called_once(self.data._item_iterator, 'a')
        self.assertEqual(
            self.data._ho_gs_lists, { 1: [], 2: ['a'], 3: ['a'] }
        )
    
    def test_map(self):
        self.data[1] = ['a', 'b', 'c']
        self.data._map_replace = Mock()
        
        def set_flag(result_container):
            self.data._replaced_an_entry = True
        
        self.data._map_replace.side_effect = set_flag
        self.data._remove_duplicates = Mock()
        self.data._remove_duplicates.return_value = sentinel.new_results
        self.data._rerank_results = Mock()
        result = self.data._map(1)
        self.assertEqual(result, sentinel.new_results)
        self.assertEqual(self.data._replaced_an_entry, True)
        self.assert_called_once(
            self.data._map_replace, ['a', 'b', 'c']
        )
        self.assert_called_once(
            self.data._remove_duplicates, ['a', 'b', 'c']
        )
        self.assert_called_once(
            self.data._rerank_results, sentinel.new_results
        )
    
    def assert_called_once(self, mock, *args, **kwds):
        self.assertEqual(mock.call_count, 1)
        self.assert_called_with(mock, [(args, kwds)])
    
    def assert_called_with(self, mock, arg_list):
        self.assertEqual(mock.call_args_list, arg_list)

if __name__ == '__main__':
    unittest.main()
