from .techniques.hierarchical_clustering import HeatMap
# from .data_source import LocalDataSource
from .data_source import RemoteDataSource
from .data_preparation import ProcessingMethod
from .configuration import Setting

SOURCE_FILE = '/home/ubuntu/lab/test.p'

if __name__ == '__main__':
    Setting.read_configuration_from_file()
    source_object = RemoteDataSource()
    print ("Total Records", source_object.get_total_record)
    fit_object = ProcessingMethod.fit_threshold(source_object.get_all_features())
    heat_map = HeatMap(fit_object)
    print heat_map.get_all_labels()
    print ("id_link", source_object.get_id_link)

    """
    source_object = LocalDataSource.get_feature_list(SOURCE_FILE)
    source_object = ProcessingMethod.fit_threshold(source_object)
    heat_map = HeatMap(source_object)
    print heat_map.get_all_labels()
    """