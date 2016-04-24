from data_mining.feature_object import DistanceObject
import numpy
from sets import Set


class HeatMap(object):

    def __init__(self, data_source):
        assert isinstance(data_source, DistanceObject)
        self.__linkage = data_source.linkage_matrix
        self.__distance_m = data_source.distance_measure
        self.__distance_max = None
        self.__distance_min = None
        self.__distance_threshold = 1
        self.__delimit = len(self.__linkage) + 1
        self.__tree_root_index = None
        self.__tree_root_structure = None

    def get_all_labels(self):
        # Lazy class
        # Use recursion to contrstruct a label (Not efficient because it cannot python recursion limit, but easy)
        # Then, I would suggest for pruning
        labels = []

        def probe(tree, chain):
            if isinstance(tree[0], tuple):
                probe(tree[0], chain + [0])
            else:
                # print (str(chain + [0]) + ":" + str(tree[0]))
                labels.append((str(chain + [0]), str(tree[0]),))

            if isinstance(tree[1], tuple):
                probe(tree[1], chain + [1])
            else:
                # print (str(chain + [1]) + ":" + str(tree[1]))
                labels.append((str(chain + [1]), str(tree[1]),))

        # tree must contain at least two branches
        if isinstance(self.root_structure, tuple):
            probe(self.root_structure, [])

        return labels

    def get_cluster_group_any(self, start_range=None, stop_range=None, cluster_diff=None):
        # define default variable
        if not start_range:
            start_range = self.distance_min
        if not stop_range:
            stop_range = self.distance_max
        if not cluster_diff:
            cluster_diff = 1

        def backward_elimination(tree, i_features):
            flat_set = Set(self.__deflate_tree(tree))
            feature_set = Set(i_features)
            inter_set = flat_set & feature_set
            ratio = float(len(inter_set)) / float(len(flat_set))

            # Recersive to each brach of the tree
            # Check for current root
            flat_set = self.__deflate_tree(tree)
            res = []

            # print flat_set
            if len(inter_set) > 0:
                # The flat list has a match, append the current one with ratio
                res += (flat_set, ratio,)
                # print ("R:", (flat_set, ratio,))
                # Check for left leave
                if isinstance(tree[0], tuple):
                    tmp = backward_elimination(tree[0], i_features)
                    # print ("tmp", tmp)
                    if tmp is not None and len(tmp) > 0:
                        res += tmp

                # Check for right leave
                if isinstance(tree[1], tuple):
                    tmp = backward_elimination(tree[1], i_features)
                    # print ("tmp", tmp)
                    if tmp is not None and len(tmp) > 0:
                        res += tmp

                    return res
            else:
                return None

        # Actual process start here
        # Get pairs from range
        pairs = self.__get_from_distance_between(start_range, stop_range)

        # Get row stat from distance matrix with threshold
        sum_stat = [0] * (self.__delimit - 1)
        for row_idx, col_idx in pairs:
            sum_stat[row_idx] += 1

        # print "Interested Features"
        # print str(sum_stat)

        # Filter interested features with threshold
        filtered_features = []
        for i, val in enumerate(sum_stat):
            if val >= cluster_diff:
                filtered_features.append(i)

        # Traverse the tree
        # print "Interested Feature with threshold"
        # print str(filtered_features)
        del sum_stat

        # print "Backward elimination"
        # t = backward_elimination(self.root_structure, filtered_features)
        # print ("T", t)
        return backward_elimination(self.root_structure, filtered_features)

    def get_best_cluster_group(self, step=0.1):
        if step >= 1.0:
            return None

        _step = (self.distance_max - self.distance_min) * step
        report = []
        for i in range(1, self.total_samples):
            # print ("current step", i , "total_sample", self.total_samples)
            current_step = self.distance_max - 0.0001
            while current_step > self.distance_min:
                res = self.get_cluster_group_any(stop_range=current_step, cluster_diff=i)

                if res:
                    accuracy = (float(i) / float(self.total_samples))
                    precision = 1.0 - (
                    float(current_step - self.distance_min) / float(self.distance_max - self.distance_min))
                    # print ("accuracy", accuracy, "precision", precision)
                    # print ("current_step", current_step, "max", self.distance_max)

                    for j in range(0, len(res), 2):
                        hit = res[j + 1]
                        report.append((res[j], hit, accuracy, precision, hit * accuracy * precision))
                        print str((self.get_label_from_samples(res[j]), self.__get_human_label_from_int(res[j])
                                   , hit, accuracy, precision, hit * accuracy * precision,
                                   current_step, self.__distance_max,
                                   i, self.total_samples), )
                        """
                        report.append({"data": res[j],
                                       "hit": hit,
                                       "accuracy": accuracy,
                                       "precision": precision,
                                       "weight": hit * accuracy * precision,
                                       "step_current": current_step,
                                       "step_max": self.__distance_max,
                                       "diff_current": i,
                                       "diff_max": self.total_samples})
                        """
                current_step -= _step

        return report

    def get_label_from_samples(self, sample_list):

        sample_set = Set(sample_list)
        if len(sample_list) == self.total_samples:
            return "root"

        def probe(tree, label):
            flatten_subtree = self.__deflate_tree(tree)
            # print ("flatten_subtree", flatten_subtree)
            if len(flatten_subtree) == len(sample_set):
                tmp_set = Set(flatten_subtree) ^ sample_set
                if len(tmp_set) == 0:
                    return label

            # probe the left branch
            tmp_res = None
            if type(tree) is not numpy.float64:
                if isinstance(tree[0], tuple):
                    tmp = probe(tree[0], label + [0])
                    if tmp:
                        tmp_res = tmp
                elif isinstance(tree[0], numpy.float64):
                    tmp = probe(tree[0], label + [0])
                    if tmp:
                        tmp_res = tmp

                # Probe the right branch
                if isinstance(tree[1], tuple):
                    tmp = probe(tree[1], label + [1])
                    if tmp:
                        tmp_res = tmp
                elif isinstance(tree[1], numpy.float64):
                    tmp = probe(tree[1], label + [1])
                    if tmp:
                        tmp_res = tmp
            else:
                return tmp_res

            return tmp_res

        label = []
        # probe the left branch
        if isinstance(self.root_structure, tuple):
            tmp = probe(self.root_structure, [])
            if tmp:
                label += tmp

        # Probe the right branch
        # if isinstance(self.root_structure[1], tuple):
        #     tmp = probe(self.root_structure[1], [1])
        #     if tmp:
        #         label += tmp

        # print ('label', label, 'sample_list',  sample_list)
        return self.__get_human_label(label)

    def map_file_index(self, file_index):
        tmp = str(self.root_structure).replace('.0', '')
        for i, item in enumerate(file_index):
            tmp = tmp.replace(str(i), item)
        return tmp

    # Service Method ---------------------------------------------------------------------------------------------------

    def __get_human_label_from_int(self, list_label):
        tmp = [int(item) for item in list_label]
        tmp = str(tmp).replace('(', '').replace(')', '').replace(' ', '') \
            .replace('[', '').replace(']', '').replace(',', '_')

        return tmp

    def __get_human_label(self, list_label):
        str_label = str(list_label).replace('(', '').replace(')', '').replace(',', '').replace(' ', '') \
            .replace('[', '').replace(']', '')

        if len(str_label) > 4:
            # Chopping it
            new_label = ""
            counter = 0
            for single_char in str_label:
                counter += 1
                new_label += single_char
                if counter % 4 == 0:
                    new_label += "-"

            if new_label[-1] == "-":
                return new_label[:-1]

            return new_label
        else:
            return str_label

    def __update_root_index(self):
        for idx, tmp in enumerate(self.__linkage):
            _, _, _, val = tmp
            val = int(val)
            if val == self.__delimit:
                self.__tree_root_index = idx
                break

    def __update_tree_structure(self):
        # read data
        def get_pair_from_tree(index):
            return int(index) - self.__delimit

        tree_like = []
        for i0, i1, i2, i3 in self.__linkage:
            if i3 == 2:
                tree_like.append((i0, i1))
            else:
                # Check for cluster
                if i0 >= self.__delimit and i1 < self.__delimit:
                    tree_like.append((tree_like[get_pair_from_tree(i0)], i1))
                    tree_like[get_pair_from_tree(i0)] = None
                elif i0 < self.__delimit and i1 >= self.__delimit:
                    tree_like.append((i0, tree_like[get_pair_from_tree(i1)]))
                    tree_like[get_pair_from_tree(i1)] = None
                else:
                    tree_like.append((tree_like[get_pair_from_tree(i0)], tree_like[get_pair_from_tree(i1)]))
                    tree_like[get_pair_from_tree(i0)] = None
                    tree_like[get_pair_from_tree(i1)] = None

        if not self.__tree_root_index:
            self.__update_root_index()

        self.__tree_root_structure = tree_like[self.__tree_root_index]

    def __get_from_distance_between(self, start_range, stop_range):
        range_pair = []
        for row_idx in range(len(self.__distance_m)):
            for col_idx in range(row_idx, len(self.__distance_m)):
                if row_idx != col_idx and \
                                self.__distance_m[row_idx][col_idx] >= start_range and \
                                self.__distance_m[row_idx][col_idx] < stop_range:
                    range_pair.append((row_idx, col_idx))

        return range_pair

    def __deflate_tree(self, tree):
        r = "[" + str(tree).replace('(', '').replace(')', '').replace(',', '').replace(' ', ', ') + "]"
        return eval(r)

    @property
    def distance_max(self):
        if not self.__distance_max:
            tmp = numpy.asarray(self.__distance_m)
            self.__distance_max = tmp.max()
            self.__distance_threshold = self.__distance_max

        return self.__distance_max

    @property
    def distance_threshold(self):
        return self.distance_max

    @property
    def distance_min(self):
        if not self.__distance_min:
            tmp = numpy.asarray(self.__distance_m)
            self.__distance_min = tmp[tmp > 0].min()

        return self.__distance_min

    @property
    def root_structure(self):
        if not self.__tree_root_structure:
            self.__update_tree_structure()

        return self.__tree_root_structure

    @property
    def total_samples(self):
        return len(self.__distance_m)