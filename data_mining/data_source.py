

class RemoteDataSource(object):
    def __init__(self):
        pass


class LocalDataSource(object):

    @staticmethod
    def get_distance_object(source_file):
        import cPickle as pickle
        from .feature_object import DistanceObject
        from data_mining.configuration import Definition
        try:
            raw_data = pickle.load(open(source_file, 'rb'))
            return DistanceObject(raw_data[Definition.DataSource.get_string_distance_measure()],
                                  raw_data[Definition.DataSource.get_string_linkage_matrix()],
                                  raw_data[Definition.DataSource.get_string_row_index()])
        except:
            raise Exception("Local data source error during initialization!")

