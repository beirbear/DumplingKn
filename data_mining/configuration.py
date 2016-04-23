class Setting(object):

    @staticmethod
    def read_configuration_from_file():
        Setting.RemoteSource.read_configuration_from_file()

    class RemoteSource(object):
        __remote_rest_addr = ''
        __remote_rest_port = ''
        __dynamic_token = ''

        @staticmethod
        def read_configuration_from_file():
            with open('configuration.json', 'rt') as t:
                data = eval(t.read())

            if 'remote_rest_addr' in data and \
                'remote_rest_port' in data and \
                'token' in data:
                try:
                    Setting.RemoteSource.__remote_rest_addr = data['remote_rest_addr']
                    Setting.RemoteSource.__remote_rest_port = data['remote_rest_port']
                    Setting.RemoteSource.__dynamic_token = data['token']
                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception("There are somethings wrong with configuration.json")

        @staticmethod
        def get_remote_address():
            return Setting.RemoteSource.__remote_rest_addr

        @staticmethod
        def get_remote_port():
            return Setting.RemoteSource.__remote_rest_port

        @staticmethod
        def get_token():
            return Setting.RemoteSource.__dynamic_token


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

        @staticmethod
        def get_string_all_feature_extension():
            return '.p.zip'

    class RemoteSource(object):
        @staticmethod
        def get_string_total_records():
            return 'http://{0}:{1}/dataRepository?token={2}&command=count'.format(
                    Setting.RemoteSource.get_remote_address(),
                    Setting.RemoteSource.get_remote_port(),
                    Setting.RemoteSource.get_token())

        @staticmethod
        def get_string_all_features():
            return 'http://{0}:{1}/dataRepository?token={2}&command=get_features'.format(
                    Setting.RemoteSource.get_remote_address(),
                    Setting.RemoteSource.get_remote_port(),
                    Setting.RemoteSource.get_token())
