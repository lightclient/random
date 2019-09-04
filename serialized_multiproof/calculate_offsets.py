import unittest
import hashlib

# 4-bit
#
#                      +--- 1 ---+
#                     /           \
#                    2             3
#                  /   \         /   \
#                 4     5       6     7
#                / \   / \     / \   / \
#               8   9 10  11  12 13 14 15
#
# 5-bit
#
#                 +-------- 1 --------+
#                /                     \
#           +-- 2 --+               +-- 3 --+
#          /         \             /         \
#         4           5           6           7
#       /   \       /   \       /   \       /   \
#      8     9     10   11     12   13     14   15
#     / \   / \   / \   / \   / \   / \   / \   / \
#    16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31

def prepare_indexes(indexes):
    raw_end_nodes = []

    # Convert index to list of bits
    for node in indexes:
        raw_end_nodes.append([1 if x == '1' else 0 for x in "{:05b}".format(node)])
    
    # Normalize input (e.g. align the most significant bit of all indexes)
    for node in raw_end_nodes:
        while node[0] == 0:
            node.pop(0)
            node.append(1)

    return raw_end_nodes


def build_offsets(nodes):
    if len(nodes) == 0 or len(nodes[0]) == 0:
        return []

    left_subtree = []
    right_subtree = []

    for node in nodes:
        if node.pop(0) == 0:
            left_subtree.append(node)
        else:
            right_subtree.append(node)

    left_subtree_size = [len(left_subtree)]
    left_subtree_offsets = build_offsets(left_subtree)
    right_subtree_offsets = build_offsets(right_subtree)   

    if len(left_subtree) == 0:
        left_subtree_size = []

    return left_subtree_size + left_subtree_offsets + right_subtree_offsets


class TestOffsetBuilder(unittest.TestCase): 
    def test_4_bit_left(self):
        nodes = prepare_indexes([8, 9, 5, 12, 13, 7])
        self.assertEqual(build_offsets(nodes), [3, 2, 1, 2, 1])

    def test_4_bit_right(self):
        nodes = prepare_indexes([4, 10, 11, 12, 13, 7])
        self.assertEqual(build_offsets(nodes), [3, 1, 1, 2, 1])

    def test_4_bit_full(self):
        nodes = prepare_indexes([8, 9, 10, 11, 12, 13, 14, 15])
        self.assertEqual(build_offsets(nodes), [4, 2, 1, 1, 2, 1, 1])

    def test_4_bit_left_small_branch(self):
        nodes = prepare_indexes([4, 10, 11, 3])
        self.assertEqual(build_offsets(nodes), [3, 1, 1])

    def test_4_bit_left_small_branch(self):
        nodes = prepare_indexes([2, 12, 13, 7])
        self.assertEqual(build_offsets(nodes), [1, 2, 1])

    def test_5_bit_left_small_branch(self):
        nodes = prepare_indexes([16, 17, 9, 5, 3])
        self.assertEqual(build_offsets(nodes), [4, 3, 2, 1])

    def test_5_bit_left_small_branch(self):
        nodes = prepare_indexes([16, 17, 9, 10, 11, 3])
        self.assertEqual(build_offsets(nodes), [5, 3, 2, 1, 1])

    def test_5_bit_right_small_branch(self):
        nodes = prepare_indexes([4, 10, 22, 23, 3])
        self.assertEqual(build_offsets(nodes), [4, 1, 1, 1])

    def test_5_bit_full(self):
        nodes = prepare_indexes(range(16, 32))
        self.assertEqual(
            build_offsets(nodes), 
            [8, 4, 2, 1, 1, 2, 1, 1, 4, 2, 1, 1, 2, 1, 1]
        )

if __name__ == '__main__':
    unittest.main()
