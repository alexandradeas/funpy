from funpy.maybe import Maybe, Just, Nothing

def test_option():
    # Maybe.of(None) returns Nothing
    assert type(Maybe[int].of(None)) == Nothing

    # Maybe.of(1) returns Just(1)
    assert type(Maybe.of(1)) == Just

def test_nothing():
    # Nothing is a subclass of Maybe
    assert issubclass(Nothing, Maybe)

    # Nothing is not a subclass of Just
    assert not issubclass(Nothing, Just)

    # Nothing is equal to itself
    assert Nothing() == Nothing()

    # is_just is False
    assert Maybe.is_just(Nothing()) == False

    # is_nothing is True
    assert Maybe.is_nothing(Nothing()) == True

    # maps a function over nothing, returning nothing
    assert Nothing[int]().map(lambda x: x + 1) == Nothing()

    # flattens nothing, returning nothing
    assert Maybe.flatten(Nothing()) == Nothing()

    # unsafe_get returns None
    try:
        Nothing().unsafe_get()
    except TypeError as e:
        assert str(e) == "cannot get value of Nothing"

    # get_or_else returns the default value
    assert Nothing[int]().get_or_else(1) == 1

    # or_else returns the default value
    assert Nothing[int]().or_else(1) == Just(1)

    # stringifies a Nothing
    assert str(Nothing()) == "Nothing()"

    # reprs a Nothing
    assert repr(Nothing()) == "Nothing()"

def test_just():
    # Just is a subclass of Maybe
    assert issubclass(Just, Maybe)

    # Just is not a subclass of Nothing
    assert not issubclass(Just, Nothing)

    # constructs a Just
    assert type(Just(1)) == Just

    # determines equality based on inner values
    assert Just(1) == Just(1)
    # determines inequality based on inner values
    assert Just(1) != Just(2)

    # is_just is True
    assert Maybe.is_just(Just(1)) == True

    # is_nothing is False
    assert Maybe.is_nothing(Just(1)) == False

    # maps a function over the value of this Just
    assert Just(1).map(lambda x: x + 1) == Just(2)

    # flattens Just(T) to T
    assert Maybe[int].flatten(Just(Just(1))) == Just(1)

    # flattens Just(Nothing) to Nothing
    assert Maybe[int].flatten(Just(Nothing())) == Nothing()

    # flattens a Just[Just[Just[T]]] to an Just[Just[T]]
    assert Maybe[Maybe[int]].flatten(Just(Just(Just(1)))) == Just(Just(1))

    # unsafe_get returns the value
    assert Just(1).unsafe_get() == 1

    # get_or_else returns the value
    assert Just(1).get_or_else(2) == 1

    # or_else returns this Just
    assert Just(1).or_else(2) == Just(1)

    # get returns the value
    assert Just(1).get() == 1

    # stringifies to "Just(value)"
    assert str(Just(1)) == "Just(1)"

    # strinifies a nested Just to "Just(Just(value))"
    assert str(Just(Just(1))) == "Just(Just(1))"

    # stringifies a nested Nothing to "Just(Nothing())"
    assert str(Just(Nothing())) == "Just(Nothing())"

    # repr is the same as str
    assert repr(Just(1)) == "Just(1)"
    assert repr(Just(Just(1))) == "Just(Just(1))"
    assert repr(Just(Nothing())) == "Just(Nothing())"


