import cPickle as pickle
import urllib2
import time
from configuration import Definition
import tarfile
import io
import zlib
import ntpath

class ParameterSweepResult():
    """ Result object to encapsulate the results of a parameter sweep at a particular parameter point along with the parameters used to compute it.

    The object has two member variables, 'result' which contains the MapReduce output and 'parameters' which is a dict containing the parameters used to compute the simulation trajectories.
    """
    def __init__(self, result, parameters):
        self.result = result
        self.parameters = parameters

    def __str__(self):
        return "{0} => {1}".format(self.parameters, self.result)

class RemoteDataSource(object):
    def __init__(self):
        """
        Test connection by get total record in the data repository
        """
        self.__total_record = None
        self.__id_link = None
        self.__update_total_record()

    @property
    def get_total_record(self):
        return self.__total_record

    def __update_total_record(self):
        req = Definition.RemoteSource.get_string_total_records()
        self.__total_record = self.__get_data(req)

    def get_all_features(self):
        req = Definition.RemoteSource.get_string_all_features()
        tmp = self.__get_data(req)
        file_like_object = io.BytesIO(tmp)
        tar = tarfile.open(fileobj=file_like_object)
        self.__id_link = list()
        data_list = []

        # use "tar" as a regular TarFile object
        for member in tar.getnames():
            # print("member", member)
            f = tar.extractfile(member).read()
            g = zlib.decompress(f)
            data_list += pickle.loads(g)
            self.__id_link.append(
                ntpath.basename(member.replace(Definition.DataSource.get_string_all_feature_extension(), '')))

        self.__total_record = len(data_list)

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

