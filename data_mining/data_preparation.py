class ProcessingMethod(object):
    """
    This class is defined as a service pool that users can add their own processing function. Many function as they want.
    """

    @staticmethod
    def fit_threshold(features):
        """
        1. Normalization
        2. Find fit threshold
        3. Distance matrix
        :return: FeatureObject()
        """
        # Standard function region -------------------------------------------------------------------------------------
        import numpy

        def normalize(data):
            std_d = numpy.std(data, axis=0)
            mean_d = numpy.mean(data, axis=0)
            return (data - mean_d) / std_d

        f_norm = normalize(features)

        from sklearn.feature_selection import VarianceThreshold

        ## Optional feature selection
        selector = VarianceThreshold()  # can give threshold parameter here, default 0 (remove all with zero variance)
        f_norm = selector.fit_transform(f_norm)

        import scipy.cluster.hierarchy as hcluster
        import scipy.spatial.distance as ssd
        from .feature_object import DistanceObject
        # cluster the rows
        row_dist = ssd.squareform(ssd.pdist(f_norm))  ## distance measure
        row_Z = hcluster.linkage(row_dist, method='single')  ## linkage matrix
        row_idxing = hcluster.leaves_list(row_Z)  ## all mean featrue vectors (leaves)
        # Standard function region -------------------------------------------------------------------------------------

        return DistanceObject(row_dist, row_Z, row_idxing)
