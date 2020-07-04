"""
Implement the Queue ADT, using a list such that the rear of the queue
is at the end of the list.
Design and implement an experiment to do benchmark comparisons of the
two queue implementations. What can you learn from such an experiment?

It is possible to implement a queue such that both enqueue and dequeue
have O(1) performance on average. In this case it means that most of
the time enqueue and dequeue will be O(1) except in one particular
circumstance where dequeue will be O(n).

```
$ python queue.py
`Queue`: Rear of the queue is at the start of the list.
enqueue time: 0.258
enqueue-dequeue time: 0.276
enqueue-dequeue-alt time: 0.318

`Queue2`: Rear of the queue is at the end of the list.
enqueue time: 0.014
enqueue-dequeue time: 0.081
enqueue-dequeue-alt time: 0.332

`Queue3`: Use 2 stacks.
enqueue time: 0.022
enqueue-dequeue time: 0.120
enqueue-dequeue-alt time: 0.676

`Queue4`: Use 2 stacks using native Python lists.
enqueue time: 0.013
enqueue-dequeue time: 0.055
enqueue-dequeue-alt time: 0.449

`Queue5`: Use collections.deque, which is a doubly linked list.
enqueue time: 0.013
enqueue-dequeue time: 0.028
```

`Queue` has O(1) enqueue, but O(N) dequeue because it has to shift
the whole list over by 1 step each time.

`Queue2` has O(N) enqueue, but O(1) dequeue.

`Queue3` and `Queue4` has O(1) enqueue. For dequeue, it is O(1) on average,
but occasionally O(N).

`Queue5` has O(1) enqueue and O(1) dequeue.
"""

# standard lib
import collections
import random
import timeit
from copy import deepcopy
from functools import partial

# first-party lib
from stack import Stack


class Queue:
	"""
	Rear of the queue is at the start of the list.
	"""
	def __init__(self):
		self.items = []

	def is_empty(self):
		return len(self.items) == 0

	def enqueue(self, item):
		self.items.insert(0, item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)


class Queue2:
	"""
	Rear of the queue is at the end of the list.
	"""
	def __init__(self):
		self.items = []

	def is_empty(self):
		return len(self.items) == 0

	def enqueue(self, item):
		self.items.append(item)

	def dequeue(self):
		return self.items.pop(0)

	def size(self):
		return len(self.items)


class Queue3:
	"""
	Use 2 stacks.
	"""
	def __init__(self):
		self.in_stack = Stack()
		self.out_stack = Stack()

	def is_empty(self):		
		return self.in_stack.is_empty() and self.out_stack.is_empty()

	def enqueue(self, item):
		self.in_stack.push(item)

	def dequeue(self):
		if self.out_stack.is_empty():
			while not self.in_stack.is_empty():
				self.out_stack.push(self.in_stack.pop())
		return self.out_stack.pop()

	def size(self):
		return self.in_stack.size() + self.out_stack.size()


class Queue4:
	"""
	Use 2 stacks using native Python lists.
	"""
	def __init__(self):
		self.in_stack = []
		self.out_stack = []

	def is_empty(self):		
		return len(self.in_stack) == 0 and len(self.out_stack) == 0

	def enqueue(self, item):
		self.in_stack.append(item)

	def dequeue(self):
		if len(self.out_stack) == 0:
			while len(self.in_stack) > 0:
				self.out_stack.append(self.in_stack.pop())
		return self.out_stack.pop()

	def size(self):
		return len(self.in_stack) + len(self.out_stack)


class Queue5:
	"""
	Use collections.deque, which is a doubly linked list.
	"""
	def __init__(self):
		self.deque = collections.deque()

	def is_empty(self):		
		return len(self.deque) == 0

	def enqueue(self, item):
		self.deque.append(item)

	def dequeue(self):
		return self.deque.popleft()

	def size(self):
		return len(self.deque)


def sim_enqueue(q_cls, n):
	q = q_cls()
	for i in range(n):
		q.enqueue(i)


def sim_enqueue_dequeue(q_cls, n):
	q = q_cls()
	for i in range(n):
		q.enqueue(i)
	for i in range(n):
		q.dequeue()

def sim_enqueue_dequeue_alt(q_cls, n):
	q = q_cls()
	for j in range(n):
		for i in range(random.randint(1, 5)):
			q.enqueue(i)
		for i in range(random.randint(1, q.size())):
			q.dequeue()


N = 10000
TIME_N = 10

def time_it(q_cls):
	t_enq = timeit.Timer(partial(sim_enqueue, q_cls, N))
	t_deq = timeit.Timer(partial(sim_enqueue_dequeue, q_cls, N))
	t_deq_alt = timeit.Timer(partial(sim_enqueue_dequeue_alt, q_cls, N))
	print(f'`{q_cls.__name__}`: {q_cls.__doc__.strip()}')
	print(f'enqueue time: {t_enq.timeit(TIME_N):.3f}')
	print(f'enqueue-dequeue time: {t_deq.timeit(TIME_N):.3f}')
	print(f'enqueue-dequeue-alt time: {t_deq_alt.timeit(TIME_N):.3f}')
	print()

time_it(Queue)
time_it(Queue2)
time_it(Queue3)
time_it(Queue4)
time_it(Queue5)

