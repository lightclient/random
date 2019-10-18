import unittest
import hashlib


def verify(offsets, proof, offset=0):
    # If `offsets` is empty, then we jumped over the end of the current
    # subtree. The current `offset` will root hash of the right subtree.
    if len(offsets) == 0:
        return proof[offset]

    left = proof[offset]
    right = proof[offset + 1]

    # If the first offset is not 1, then we have not reached an end node
    # so continue to recurse.
    if offsets[0] != 1:
        left = verify(
            # Pass in the offsets only for the left subtree. 
            offsets[1:(offsets[0])],
            proof,
            offset,
        )
    
    # If there is only 1 offset, then we can be sure that we've reached the
    # bottom of the subtree and the right node can be inferred as
    # left_offset + 1, Otherwise, recurse on the right side.
    if len(offsets) != 1:
        right = verify(
            # Pass in the offsets only for the right subtree.
            offsets[offsets[0]:],
            proof,
            offsets[0] + offset,
        )

    return hash(left, right)


def hash(left, right):
    hasher = hashlib.sha256()
    hasher.update(bytes.fromhex(left))
    hasher.update(bytes.fromhex(right))
    return hasher.hexdigest()


def zh(depth):
    if depth == 0:
        return "00" * 32

    h = zh(depth - 1)

    return hash(h, h)


class TestOffsetBuilder(unittest.TestCase): 
    def test_simple(self):
        # indexes = [4, 10, 11, 3]
        offsets = [3, 1, 1]
        proof = [zh(1), zh(0), zh(0), zh(2)]

        self.assertEqual(verify(offsets, proof), zh(3))

    def test_full(self):
        # indexes = [8, 9, 10, 11, 12, 13, 14, 15]
        offsets = [4, 2, 1, 1, 2, 1, 1]
        proof = [zh(0)] * 8

        self.assertEqual(verify(offsets, proof), zh(3))

    def test_random(self):
        # indexes = [2, 12, 26, 27, 7]
        offsets = [1, 3, 1, 1]
        proof = [
            hash("01", "02"), 
            hash("03", "04"),
            hash("05", "06"),
            hash("07", "08"),
            hash("09", "0A"),
        ]

        root = hash(proof[0], 
                    hash(
                        hash(proof[1], 
                            hash(proof[2], proof[3])
                        ), 
                        proof[4]
                    )
                )

        self.assertEqual(verify(offsets, proof), root)

    def test_large(self):
        # indexes = [2, 6, 7168, 7169, 3585, 1793, 897, 449, 225, 113, 57, 29, 15]
        offsets = [1, 1, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        proof = [
                zh(11),
                zh(10),
                zh(0),
                zh(0),
                zh(1),
                zh(2),
                zh(3),
                zh(4),
                zh(5),
                zh(6),
                zh(7),
                zh(8),
                zh(9),
        ]

        self.assertEqual(verify(offsets, proof), zh(12))

if __name__ == '__main__':
    unittest.main()
