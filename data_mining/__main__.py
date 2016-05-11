"""
Application entry point.
"""

from .techniques.hierarchical_clustering import HeatMap
from .data_source import RemoteDataSource
from .data_preparation import ProcessingMethod
from .configuration import Setting, Definition
import time

if __name__ == '__main__':

    # Read configuration from file
    Setting.read_configuration_from_file()
    counter = 0

    while True:
        source_object = RemoteDataSource()

        if isinstance(source_object.total_record, str):
            print "No data... skip"
            time.sleep(60)
            continue

        """The data source should be repeated check for update from the data repository."""

        # Check total records for test connection
        print ("Total Records", source_object.total_record)

        # Pre-processing data
        fit_object = ProcessingMethod.fit_threshold(source_object.get_all_features())

        # Generate distance matrix
        heat_map = HeatMap(fit_object)

        # Push linkage matrix back
        source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_linkage_matrix(),
                                        fit_object.linkage_matrix)
        # Push row_index back
        source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_row_index(),
                                        source_object.id_link)
        # Push label_tree back
        source_object.push_to_data_repo(Definition.RemoteSource.get_string_push_label_tree(),
                                        heat_map.get_all_labels())

        counter += 1
        print "Finish iteration, ", str(counter)

        if source_object.total_record == 1000:
            break

        time.sleep(60)
