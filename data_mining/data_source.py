from configuration import Definition
import cPickle as pickle
import urllib2
import time
import tarfile
import io
import zlib
import ntpath
import json
import numpy


class ParameterSweepResult():
    """
    Result object to encapsulate the results of a parameter sweep at a particular parameter point along with the
    parameters used to compute it. The object has two member variables, 'result' which contains the MapReduce output
    and 'parameters' which is a dict containing the parameters used to compute the simulation trajectories.
    """
    def __init__(self, result, parameters):
        self.result = result
        self.parameters = parameters

    def __str__(self):
        return "{0} => {1}".format(self.parameters, self.result)


class RemoteDataSource(object):
    """
    RemoteDataSource is used for connect to a remote data source. This class will be used to get the data from the
    data repository.
    """

    def __init__(self):
        """
        Test connection by get total record in the data repository
        """
        self.__total_record = None
        self.__id_link = None
        self.__update_total_record()

    @property
    def total_record(self):
        return self.__total_record

    @property
    def id_link(self):
        return self.__id_link

    def get_all_features(self):
        """
        Purpose: This function is used to get the data from the remote data source.
        """
        # Get data from remote source into tmp
        tmp = self.__get_data(Definition.RemoteSource.get_string_all_features())

        # Create a variable to hold the tar file
        file_like_object = io.BytesIO(tmp)
        tar = tarfile.open(fileobj=file_like_object)

        # Create an empty variables to hold the result
        self.__id_link = list()
        data_list = []

        # use "tar" as a regular TarFile object
        for member in tar.getnames():
            f = tar.extractfile(member).read()
            g = zlib.decompress(f)
            data_list.append(pickle.loads(g))
            self.__id_link.append(
                ntpath.basename(member.replace(Definition.DataSource.get_string_all_feature_extension(), '')))

        # Update total records
        self.__total_record = len(data_list)

        return data_list

    def push_to_data_repo(self, command, content):
        """
        Purpose: This function push the data to back to the server.
        """

        # Define component for pushing data
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)

        # Get a push request string
        url = Definition.RemoteSource.get_string_push_data(command)

        def send_data_to_repo():
            """
            The actual function that send the data to the server.
            """
            if isinstance(content, numpy.ndarray):
                request = urllib2.Request(url, data=json.dumps(content.tolist()))
            else:
                request = urllib2.Request(url, data=json.dumps(content))

            request.add_header("Content-Type", 'application/json')
            request.get_method = lambda: method

            try:
                connection = opener.open(request)
            except urllib2.HTTPError, e:
                connection = e

            if connection.code == Definition.DataSource.get_success_return_code():
                return True

            return False

        # Repeatedly push the data to server. No process termination.
        while not send_data_to_repo():
            time.sleep(5)

    # Internal Service Class ------------------------------------------------
    def __update_total_record(self):
        """
        Internal function for update total records.
        """
        req = Definition.RemoteSource.get_string_total_records()
        self.__total_record = int(self.__get_data(req).replace("Total records:"))

    def __get_data(self, request_url):
        """
        Purpose: This function get a data from a remtoe source.
        :return: data from push request
        """
        data = None

        """Define a function that get a data from server via REST."""
        def send_data_to_repo():
            req = urllib2.Request(request_url)
            response = urllib2.urlopen(req)

            if response.code == 200:
                data = response.read()
            else:
                return None

            return data

        """Repeatedly send a get-request to server."""
        is_repeat = True
        while is_repeat:
            data = send_data_to_repo()
            if data:
                is_repeat = False
            else:
                time.sleep(5)

        return data

    # Internal Service Class --------------------------------------------------


class LocalDataSource(object):
    """
    This class is used for testing the flow. Not use for production
    """
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

