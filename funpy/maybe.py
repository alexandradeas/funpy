from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, TypeVar, TypeGuard, NoReturn


T = TypeVar('T')
G = TypeVar('G')

class Maybe(ABC, Generic[T]):
    """
    Maybe is a container for a value that may or may not exist

    This class is abstract, and should not be instantiated directly. Instead,
    use the static method Maybe.of which will return a Just or Nothing if the
    value is not None or None, respectively. Just.of and Nothing.of are also
    provided for convenience.
    """
    @staticmethod
    def of(value: T | None) -> "Maybe[T]":
        """
        constructs an Maybe from a value
        Just(value) if value is not None
        Nothing() if value is None
        """
        if value == None:
            return Nothing()
        else:
            return Just(value)

    @staticmethod
    def just(value: T) -> "Just[T]":
        """
        constructs a Just(value)
        """
        return Just(value)

    @staticmethod
    def nothing() -> "Nothing[T]":
        """
        constructs a Nothing()
        """
        return Nothing()

    @staticmethod
    def flatten(option: "Maybe[Maybe[T]]") -> "Maybe[T]":
        """
        flattens an Maybe[Maybe[T]] to an Maybe[T]
        if this is Nothing then the result is Nothing
        otherwise the result is the inner Maybe
        """
        return option.get_or_else(Nothing())

    @staticmethod
    def is_just(option: "Maybe[T]") -> TypeGuard["Just[T]"]:
        """
        returns True if option is Just, False otherwise
        """
        return type(option) == Just

    @staticmethod
    def is_nothing(option: "Maybe[T]") -> TypeGuard["Nothing[T]"]:
        """
        returns True if option is Nothing, False otherwise
        """
        return type(option) == Nothing

    @abstractmethod
    def map(self, f: Callable[[T], G]) -> "Maybe[G]":
        """
        maps a function over the value of this Maybe
        if this is Nothing then the result is Nothing
        if the value returned from f is None, then the result is Nothing
        otherwise the result is Just(f(value))
        """

    @abstractmethod
    def fold(self, f: Callable[[T, G], G], initial: G) -> G:
        """
        folds over the value of this Maybe
        if this is Nothing then the result is initial
        otherwise the result is f(value, initial)
        """

    @abstractmethod
    def unsafe_get(self) -> T:
        """
        returns the value of this Maybe if it is Just, otherwise raises a TypeError
        """

    @abstractmethod
    def get_or_else(self, otherwise: T) -> T:
        """
        returns the value of this Maybe if it is Just, else returns otherwise
        """

    @abstractmethod
    def or_else(self, otherwise: T) -> "Just[T]":
        """
        returns this Maybe if it is Just, else returns a Just containing otherwise
        """

    @abstractmethod
    def as_nullable(self) -> Optional[T]:
        """
        returns the value of this Maybe if it is Just, else returns None
        """

class Just(Maybe[T]):
    def __init__(self, value: T):
        """
        constructs a Just(value)
        """
        self.__value = value

    def __eq__(self, other: object) -> bool:
        if type(other) == Just:
            # pyright doesn't know what T is in other, that's not a problem
            # here because we are checking whether the values are equal
            return self.__value == other.unsafe_get() # type: ignore
        return False

    def map(self, f: Callable[[T], G]) -> "Just[G]":
        return Just(f(self.__value))

    def fold(self, f: Callable[[T, G], G], initial: G) -> G:
        return f(self.__value, initial)

    def get(self):
        return self.__value

    def unsafe_get(self):
        return self.__value

    def get_or_else(self, otherwise: T) -> T:
        return self.__value

    def or_else(self, otherwise: T) -> "Just[T]":
        return self

    def as_nullable(self) -> T:
        return self.__value

    def __str__(self):
        return "Just({})".format(self.__value)

    def __repr__(self) -> str:
        return self.__str__()

class Nothing(Maybe[T]):
    def __eq__(self, other: object) -> bool:
        return type(other) == Nothing

    def map(self, f: Callable[[T], G]) -> "Nothing[G]":
        return Nothing()

    def fold(self, f: Callable[[T, G], G], initial: G) -> G:
        return initial

    def unsafe_get(self) -> NoReturn:
        raise TypeError("cannot get value of Nothing")

    def get_or_else(self, otherwise: T) -> T:
        return otherwise

    def or_else(self, otherwise: T) -> Just[T]:
        return Just(otherwise)

    def as_nullable(self) -> None:
        return None

    def __str__(self) -> str:
        return "Nothing()"

    def __repr__(self) -> str:
        return self.__str__()

# register Just and Nothing as subclasses of Maybe
Maybe.register(Just)
Maybe.register(Nothing)

