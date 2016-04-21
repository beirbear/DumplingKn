import cPickle as pickle
import urllib2
import time
from configuration import Definition


class RemoteDataSource(object):
    def __init__(self):
        """
        Test connection by get total record in the data repository
        """
        req = Definition.RemoteSource.get_string_total_records()
        self.__total_record = self.__get_data(req)
        self.__id_link = None

    @property
    def get_total_record(self):
        return self.__total_record

    @property
    def get_all_features(self):
        req = Definition.RemoteSource.get_string_all_features()
        tmp = eval(self.__get_data(req))
        # Convert dict into list and store the id with index
        self.__id_link = list()
        data_list = []

        for key, value in tmp:
            data_list += value
            self.__id_link.append(key)

        return data_list

    @property
    def get_id_link(self):
        return self.__id_link


    # Internal Service Class ------------------------------------------------
    def __get_data(self, request_url):
        data = None

        def send_data_to_repo(request_url):
            req = urllib2.Request(request_url)
            response = urllib2.urlopen(req)

            if response.code == 200:
                data = response.read()
            else:
                return None

            return data

        is_repeat = True
        while is_repeat:
            data = send_data_to_repo(request_url)
            if data:
                is_repeat = False
            else:
                time.sleep(5)

        return data
    # Internal Service Class --------------------------------------------------


class LocalDataSource(object):

    @staticmethod
    def get_feature_list(source_file):
        try:
            return pickle.load(open(source_file, 'rb'))
        except:
            raise Exception("Local data source error during initialization!")

    @staticmethod
    def get_distance_object(source_file):
        from .feature_object import DistanceObject
        from data_mining.configuration import Definition
        try:
            raw_data = pickle.load(open(source_file, 'rb'))
            return DistanceObject(raw_data[Definition.DataSource.get_string_distance_measure()],
                                  raw_data[Definition.DataSource.get_string_linkage_matrix()],
                                  raw_data[Definition.DataSource.get_string_row_index()])
        except:
            raise Exception("Local data source error during initialization!")

