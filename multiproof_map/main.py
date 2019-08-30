#
#         +--- 1 ---+
#        /           \
#       2             3
#     /   \         /   \
#    4     5       6     7
#   / \   / \     / \   / \
#  8   9 10  11  12 13 14 15
#
#  Proving 8, 13 => needs 8, 9, 12, 13, 5, 7
#
#  Serialized: [2, skip, 1, 2, skip, 1] [h[8], h[9], h[12], h[13]]
#
#   8 => 1000
#   9 => 1001
#  12 => 1100
#  13 => 1101

BIT_LENGTH = 4

end_nodes = [8, 9, 12, 13]
raw_end_nodes = []
for node in end_nodes:
    raw_end_nodes.append([1 if x == '1' else 0 for x in "{:04b}".format(node)])

map = []


stack = [[len(raw_end_nodes) - 1] + raw_end_nodes]

while len(stack) > 0:
    current = stack.pop(0)
    bits = current.pop(0)

    print("stack: " + str(stack))
    print("bits : " + str(bits))

    for bit in range(0, bits):
        left = 0
        right = [BIT_LENGTH - bit]

        print("Current bit : " + str(bit))

        for node in current:
            print("Current node: " + str(node))

            if node[bit] == 0:
                left += 0
            else:
                right.append(node)

        map.append(left)

        if bit == bits:
            stack.append(right)

        print("left: " + str(left))


print(map)
