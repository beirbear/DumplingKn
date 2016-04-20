from .techniques.hierarchical_clustering import HeatMap
from .data_source import LocalDataSource

SOURCE_FILE = '/Users/beir/Downloads/sandbox/linkage.p'

if __name__ == '__main__':
    source_object = LocalDataSource.get_distance_object(SOURCE_FILE)
    heat_map = HeatMap(source_object)
