from funpy.node import Node
from funpy.maybe import Just, Nothing

def test_node():
    # next is Nothing when not initialized
    assert Node(1).get() == (1, Nothing())

    # next is Just when initialized
    assert Node(1, Node(2)).get() == (1, Just(Node(2)))

    # map returns a new node with each node mapped by f
    assert Node(1, Node(2)).map(lambda x: x + 1) == Node(2, Node(3))
    assert Node(1, Node(2, Node(3))).map(lambda x: x + 1) == Node(2, Node(3, Node(4)))

    # is equal to itself
    assert Node(1) == Node(1)
    assert Node(1, Node(2)) == Node(1, Node(2))
    assert Node(1) != Node(2)
    assert Node(1, Node(2)) != Node(1, Node(3))

    # iterates over values in the list
    assert list(Node(1, Node(2))) == [1, 2]
    for i, node in enumerate(Node(1, Node(2, Node(3, Node(4, Node(5)))))):
        assert node == i + 1

    # Node.of constructs a Node's from infinitary arguments
    assert Node.of(1, 2, 3, 4, 5) == Node(1, Node(2, Node(3, Node(4, Node(5)))))
