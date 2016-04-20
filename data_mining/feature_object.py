

class DistanceObject(object):
    def __init__(self, distance_measure, linkage_matrix, row_index):
        self._distance_measure = distance_measure
        self._linkage_matrix = linkage_matrix
        self._row_index = row_index

    @property
    def distance_measure(self):
        return self._distance_measure

    @property
    def linkage_matrix(self):
        return self._linkage_matrix

    @property
    def row_index(self):
        return self._row_index
