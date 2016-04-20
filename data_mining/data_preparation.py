class ProcessingMethod(object):
    """
    This class is defined as a service pool that users can add their own processing function. Many function as they want.
    """

    @staticmethod
    def fit_threshold(ret):
        """
        1. Normalization
        2. Find fit threshold
        3. Distance matrix
        :return: FeatureObject()
        """
        # Standard function region -------------------------------------------------------------------------------------
        import numpy
        import numpy as np
        import sklearn.preprocessing
        import sklearn

        def replace_nan(X):
            """ Replaces NaN values with the feature (column) mean. If the feature column also contains an odd number of +-Inf the mean
            will become +-Inf. This is ok for now since we will replace those values when rescale the data. """
            X = np.asarray(X)
            nans = []
            for c, v in enumerate(X):
                for p, a in enumerate(v):
                    if numpy.isnan(a):
                        nans.append((c, p))
            for es, f in nans:
                m = np.mean(np.nan_to_num(X[:, f]))
                X[es, f] = m
            return X

        features = []

        for n, pp in enumerate(ret):
            f_set = []
            for r, es in enumerate(pp.result):
                f_set.append(es['features'])

            f_set = replace_nan(f_set)  # repalce NaNs with mean
            # f_set = np.nan_to_num(f_set)
            mm_scale = sklearn.preprocessing.MinMaxScaler()  # scale the data, thiswill remove +-inf
            f_set = mm_scale.fit_transform(f_set)
            m = np.mean(f_set, axis=0)
            features.append(m)

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
