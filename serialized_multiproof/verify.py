import unittest
import hashlib


def verify(offsets, proof, offset=0):
    if len(offsets) == 0:
        return proof[offset]

    left = proof[offset]
    right = proof[offset + 1]

    # If the first offset is not one, then we have not reached an end node
    # so continue to recurse.
    if offsets[0] != 1:
        left = verify(
            offsets[1:(offsets[0])],
            proof,
            offset,
        )
    
    # If there is only 1 offset, then we can be sure that we've reached the
    # bottom of the tree and the right node can be inferred as left_offset + 1,
    # Otherwise, recurse on the right side.
    if len(offsets) != 1:
        right = verify(
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
        return "0" * 64

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

if __name__ == '__main__':
    unittest.main()
