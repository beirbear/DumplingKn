from .techniques.hierarchical_clustering import HeatMap
from .data_source import LocalDataSource
from .data_preparation import ProcessingMethod

SOURCE_FILE = '/home/ubuntu/lab/test.p'

if __name__ == '__main__':
    source_object = LocalDataSource.get_distance_object(SOURCE_FILE)
    source_object = ProcessingMethod.fit_threshold(source_object)
    heat_map = HeatMap(source_object)
    print heat_map.get_all_labels()