class Setting(object):
    pass


class Definition(object):
    class DataSource(object):
        @staticmethod
        def get_string_distance_measure():
            return 'row_dist'

        @staticmethod
        def get_string_linkage_matrix():
            return 'row'

        @staticmethod
        def get_string_row_index():
            return 'index'

    """
    class DataRepository:
        __count_records = 'localhost:8100/dataRepository?token=None&command=count'
        __get_features = 'localhost:8100/dataRepository?token=None&command=get_features'
    """