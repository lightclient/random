import unittest
import hashlib


def verify(offsets, proof, offset=0):
    if len(offsets) == 0:
        return proof[offset]

    if offsets[0] == 1:
        left = proof[offset]
        right = proof[offset + 1]

        if len(offsets) != 1:
            right = verify(
                offsets[offsets[0]:],
                proof,
                offsets[0] + offset,
            )

        return hash(left, right)

    left = verify(
        offsets[1:(offsets[0])],
        proof,
        offset,
    )

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
        offsets = [3, 1, 1]
        proof = [zh(1), zh(0), zh(0), zh(2)]
        self.assertEqual(verify(offsets, proof), zh(3))

if __name__ == '__main__':
    unittest.main()
