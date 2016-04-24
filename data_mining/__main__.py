from .techniques.hierarchical_clustering import HeatMap
# from .data_source import LocalDataSource
from .data_source import RemoteDataSource
from .data_preparation import ProcessingMethod
from .configuration import Setting, Definition

SOURCE_FILE = '/home/ubuntu/lab/test.p'

if __name__ == '__main__':
    Setting.read_configuration_from_file()
    source_object = RemoteDataSource()
    print ("Total Records", source_object.get_total_record)
    fit_object = ProcessingMethod.fit_threshold(source_object.get_all_features())
    heat_map = HeatMap(fit_object)

    # Push linkage matrix back
    source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_linkage_matrix(),
                                    fit_object.linkage_matrix)
    # Push row_index back
    source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_row_index(),
                                    source_object.get_id_link)
    # Push label_tree back
    source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_label_tree(),
                                    heat_map.get_all_labels())

    """
    source_object = LocalDataSource.get_feature_list(SOURCE_FILE)
    source_object = ProcessingMethod.fit_threshold(source_object)
    heat_map = HeatMap(source_object)
    print heat_map.get_all_labels()
    """