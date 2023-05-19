from funpy.maybe import Maybe, Nothing
from typing import Callable, Generic, Iterator, TypeVar, Optional

T = TypeVar('T')
G = TypeVar('G')

class Node(Generic[T]):
    """
    Node is an immutable container for a value and a reference to the next node

    This class is generic, and should be instantiated with a type parameter
    that matches the type of the value contained in the node.
    """
    def __init__(self, value: T, next: Optional["Node[T]"] = None):
        self.__value: T = value
        self.__next: Maybe["Node[T]"] = Maybe.of(next)

    @staticmethod
    def of(*values: T) -> "Node[T]":
        """
        constructs a Node from a list of values
        """
        if len(values) == 0:
            raise ValueError("Cannot construct a Node from an empty list")

        # constructs a chain of nodes from back-to-front by starting with the
        # last value and then prepending the next node to the front
        tail: Node[T] = Node(values[-1], next = None)
        for value in reversed(values[:-1]):
            tail = Node(value, tail)
        return tail

    def __eq__(self, other: object) -> bool:
        """
        returns True if other is a Node with the same value and next, False otherwise
        """
        if not isinstance(other, Node):
            return False
        # pyright is not able to get over the fact that Node[Unknown] includes
        # an Unknown. Doesn't matter in this case because we're just checking
        # the types, if they're not the same then there's no point comparing
        # them
        elif type(other.get()) != type(self.get()): # type: ignore
            return False
        
        # compares the entire chain by recursively calling __eq__ on the next
        # node by calling get
        return other.get() == self.get()

    def __iter__(self) -> Iterator[T]:
        """
        returns an iterator over the nodes in this list
        """
        yield self.__value
        if Maybe.is_some(self.__next):
            yield from self.__next.get()


    def map(self, f: Callable[[T], G]) -> "Node[G]":
        """
        Returns a new Node with the value of this node mapped by f
        """
        return Node(
            f(self.__value),
            self.__next.map(lambda node: node.map(f)).as_nullable()
        )
    
    def fold(self, f: Callable[[T, G], G], initial: G) -> G:
        """
        Folds over the nodes in this list
        """
        return self.__next.fold(
            lambda node, acc: node.fold(
                f,
                f(node.get_value(), acc)
            ),
            f(self.__value, initial)
        )

    def get(self) -> tuple[T, Maybe["Node[T]"]]:
        """
        Returns a tuple of the value of this node and the next node
        """
        return (self.__value, self.__next)

    def get_value(self) -> T:
        """
        Gets the value of this node
        """
        return self.__value

    def get_next(self) -> Maybe["Node[T]"]:
        """
        Gets the next node
        """
        return self.__next

    def __repr__(self) -> str:
        return "Node({}, {})".format(self.__value, self.__next)

    def __str__(self) -> str:
        return self.__repr__()

