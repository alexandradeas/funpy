from typing import Generic, TypeVar
from funpy.maybe import Maybe, Just, Nothing
from funpy.node import Node

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, max_size: int = 0):
        """
        constructs a Stack with a maximum size of max_size

        If max_size is 0 then the stack is unbounded
        """
        if max_size < 0:
            raise ValueError("max_size must be non-negative")

        self.__max_size: int = max_size
        self.__head: Maybe[Node[T]] = Nothing()
        self.__size: int = 0

    def push(self, value: T) -> None:
        if self.__max_size != 0 and self.__size >= self.__max_size:
            raise ValueError("stack is full")
        elif self.__size == 0:
            self.__head: Maybe[Node[T]] = Just(Node(value))
        else:
            self.__head: Maybe[Node[T]] = Just(Node(value, self.__head.unsafe_get()))
        self.__size += 1

    def pop(self) -> Maybe[T]:
        if Maybe.is_nothing(self.__head):
            return Nothing[T]()
        self.__size -= 1
        head_value, self.__head = self.__head.unsafe_get().get()
        return Just(head_value)


    def peek(self) -> Maybe[T]:
        if Maybe.is_nothing(self.__head):
            return Nothing[T]()
        return Just(self.__head.unsafe_get().get_value())

    def size(self) -> int:
        return self.__size
