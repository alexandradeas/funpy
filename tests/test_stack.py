from funpy.stack import Stack
from funpy.maybe import Just, Nothing

def test_stack_push_pop():
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == Just(3)
    assert stack.pop() == Just(2)
    assert stack.pop() == Just(1)
    assert stack.pop() == Nothing()

def test_stack_peek():
    stack = Stack[int]()
    stack.push(1)
    assert stack.peek() == Just(1)
    stack.push(2)
    assert stack.peek() == Just(2)
    stack.push(3)
    assert stack.peek() == Just(3)

def test_stack_max_size():
    # creates a new stack with a maximum size of 10
    stack = Stack[int](10)
    for i in range(1, 11):
        stack.push(i)
        assert stack.size() == i

    assert stack.size() == 10

    try:
        stack.push(11)
    except ValueError as e:
        assert str(e) == "stack is full"

    # pop a value then push a value to make sure the stack is still usable

    assert stack.pop() == Just(10)
    assert stack.size() == 9

    stack.push(11)

    assert stack.size() == 10




