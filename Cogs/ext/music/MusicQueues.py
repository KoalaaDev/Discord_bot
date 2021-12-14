from asyncio import Queue
from pomice.objects import Track 
from typing import (
    AsyncIterator,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from copy import copy

class HistoryQueue(Queue):
    def __str__(self) -> str:
        """String showing all Playable objects appearing as a list."""
        return str(list(f"'{t}'" for t in self))

    def __repr__(self) -> str:
        """Official representation with max_size and member count."""
        return (
            f"<{self.__class__.__name__} max_size={self.maxsize} members={self.count}>"
        )

    def __bool__(self) -> bool:
        """Treats the queue as a bool, with it evaluating True when it contains members."""
        return bool(self.count)

    def __call__(self, item: Track) -> None:
        """Allows the queue instance to be called directly in order to add a member."""
        self.put(item)

    def __len__(self) -> int:
        """Return the number of members in the queue."""
        return self.count

    def __getitem__(self, index: int) -> Track:
        """Returns a member at the given position.
        Does not remove item from queue.
        """
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        return self._queue[index]

    def __setitem__(self, index: int, item: Track):
        """Inserts an item at given position."""
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        self.put_at_index(index, item)

    def __delitem__(self, index: int) -> None:
        """Delete item at given position."""
        self._queue.__delitem__(index)

    def __iter__(self) -> Iterator[Track]:
        """Iterate over members in the queue.
        Does not remove items when iterating.
        """
        return self._queue.__iter__()

    def __reversed__(self) -> Iterator[Track]:
        """Iterate over members in reverse order."""
        return self._queue.__reversed__()

    def __contains__(self, item: Track) -> bool:
        """Check if an item is a member of the queue."""
       
class MusicQueue(Queue):
    
    def __str__(self) -> str:
        """String showing all Playable objects appearing as a list."""
        return str(list(f"'{t}'" for t in self))

    def __repr__(self) -> str:
        """Official representation with max_size and member count."""
        return (
            f"<{self.__class__.__name__} max_size={self.maxsize} members={self.count}>"
        )

    def __bool__(self) -> bool:
        """Treats the queue as a bool, with it evaluating True when it contains members."""
        return bool(self.count)

    def __call__(self, item: Track) -> None:
        """Allows the queue instance to be called directly in order to add a member."""
        self.put(item)

    def __len__(self) -> int:
        """Return the number of members in the queue."""
        return self.count

    def __getitem__(self, index: int) -> Track:
        """Returns a member at the given position.
        Does not remove item from queue.
        """
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        return self._queue[index]

    def __setitem__(self, index: int, item: Track):
        """Inserts an item at given position."""
        if not isinstance(index, int):
            raise ValueError("'int' type required.'")

        self.put_at_index(index, item)

    def __delitem__(self, index: int) -> None:
        """Delete item at given position."""
        self._queue.__delitem__(index)

    def __iter__(self) -> Iterator[Track]:
        """Iterate over members in the queue.
        Does not remove items when iterating.
        """
        return self._queue.__iter__()

    def __reversed__(self) -> Iterator[Track]:
        """Iterate over members in reverse order."""
        return self._queue.__reversed__()

    def __contains__(self, item: Track) -> bool:
        """Check if an item is a member of the queue."""
        return item in self._queue

    def __add__(self, other: Iterable[Track]) -> Queue:
        """Return a new queue containing all members.
        The new queue will have the same max_size as the original.
        """
        if not isinstance(other, Iterable):
            raise TypeError(f"Adding with the '{type(other)}' type is not supported.")

        new_queue = self.copy()
        new_queue.extend(other)
        return new_queue

    def __iadd__(self, other: Union[Iterable[Track], Track]) -> Queue:
        """Add items to queue."""
        if isinstance(other, Track):
            self.put(other)
            return self

        if isinstance(other, Iterable):
            self.extend(other)
            return self

        raise TypeError(f"Adding '{type(other)}' type to the queue is not supported.")

    def _get(self) -> Track:
        return self._queue.popleft()

    def _drop(self) -> Track:
        return self._queue.pop()

    def _index(self, item: Track) -> int:
        return self._queue.index(item)

    def _put(self, item: Track) -> None:
        self._queue.append(item)

    def _insert(self, index: int, item: Track) -> None:
        self._queue.insert(index, item)

    @staticmethod
    def _check_playable(item: Track) -> Track:
        if not isinstance(item, Track):
            raise TypeError("Only Playable objects are supported.")

        return item

    @classmethod
    def _check_playable_container(cls, iterable: Iterable) -> List[Track]:
        iterable = list(iterable)
        for item in iterable:
            cls._check_playable(item)

        return iterable

    @property
    def count(self) -> int:
        """Returns queue member count."""
        return len(self._queue)

    @property
    def is_empty(self) -> bool:
        """Returns True if queue has no members."""
        return not bool(self.count)

    @property
    def is_full(self) -> bool:
        """Returns True if queue item count has reached max_size."""
        return False if self.maxsize is None else self.count >= self.maxsize

    async def get(self) -> Track:
        """Return next immediately available item in queue if any.
        Raises QueueEmpty if no items in queue.
        """
        if self.is_empty:
            raise "No items in the queue."

        return self._get()

    async def pop(self) -> Track:
        """Return item from the right end side of the queue.
        Raises QueueEmpty if no items in queue.
        """
        if self.is_empty:
            raise "No items in the queue."

        return self._queue.pop()

    async def find_position(self, item: Track) -> int:
        """Find the position a given item within the queue.
        Raises ValueError if item is not in queue.
        """
        return self._index(self._check_playable(item))

    async def put(self, item: Track) -> None:
        """Put the given item into the back of the queue."""
        return self._put(self._check_playable(item))

    async def put_at_index(self, index: int, item: Track) -> None:
        """Put the given item into the queue at the specified index."""

        return self._insert(index, self._check_playable(item))

    async def put_at_front(self, item: Track) -> None:
        """Put the given item into the front of the queue."""
        return self.put_at_index(0, item)
    def copy(self) -> Queue:
        """Create a copy of the current queue including it's members."""
        new_queue = self.__class__(max_size=self.maxsize)
        new_queue._queue = copy(self._queue)

        return new_queue

    async def clear(self) -> None:
        """Remove all items from the queue."""
        self._queue.clear()