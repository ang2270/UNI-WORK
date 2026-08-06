from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None, internal_sizes=None):
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = None
        self.size_index = 0
        self.count = 0
        self.my_array: ArrayR[tuple[K1 | K2, V]] = ArrayR(self.TABLE_SIZES[self.size_index])

    
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.TABLE_SIZES[self.size_index]

    
    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        top_level_index = self.hash1(key1)  # get index for first key

        for _ in range(self.table_size):
            top_level_table_entry = self.my_array[top_level_index]
            if top_level_table_entry is None:  # checks if entry is empty
                if is_insert:  # if true, new key-value is being inserted
                    self.count += 1
                    sub_table = LinearProbeTable(sizes=self.internal_sizes)
                    sub_table.hash = lambda k: self.hash2(k, sub_table)
                    sub_table_index = self.hash2(key2, sub_table)
                    self.my_array.array[top_level_index] = (key1, sub_table)  # associates the sub table to the key from top_index
                    return top_level_index, sub_table_index  # since first entry we return the top level and sub level index (0 since top_level_entry is none)
                else:
                    raise KeyError((key1, key2))  # key doesn't exist
            else:  # already an entry for key
                key1_existing, sub_table = top_level_table_entry  # Gets the key, value from the table
                if key1_existing == key1:  # Check for matching keys
                    sub_table_index = self.hash2(key2, sub_table)  # if matching, finds the hash index for key2 in the sub table
                    for _ in range(sub_table.table_size):  # finds a position for key2 using linear probing
                        if sub_table.array[sub_table_index] is None:  # if position is empty
                            if is_insert:  # and inserting
                                return top_level_index, sub_table_index  # top and sub level index's
                            else:
                                raise KeyError((key1, key2))  # key2 doesnt exist
                        elif sub_table.array[sub_table_index][0] == key2:  # not empty but key's match
                            return top_level_index, sub_table_index  # top and sub level index's
                        else:
                            sub_table_index = (sub_table_index + 1) % sub_table.table_size  # Linear probing increments

                    if is_insert:  # after for loop if true
                        raise FullError("Sub-table is full!")
                    else:
                        raise KeyError((key1, key2))  # (key1, key2) doesn't exist in the table

            top_level_index = (top_level_index + 1) % self.table_size  # Linear probe for the high-level key

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError((key1, key2))

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for entry in self.my_array.array:
                if entry is not None:
                    yield entry[0]
        else:
            top_level_index = self.hash1(key)
            top_level_table_entry = self.my_array.array[top_level_index]
            if top_level_table_entry is not None and top_level_table_entry[0] == key:
                sub_table_iter = top_level_table_entry[1].iter_keys()
                for sub_key in sub_table_iter:
                    yield sub_key

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        """ 
        def keys(self) -> list[K]
        Returns all keys in the hash table.
        :complexity: O(N) where N is self.table_size.
        
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res"""

        if key is None:
            return [entry[0] for entry in self.my_array.array if entry is not None]
        else:
            for entry in self.my_array.array:
                if entry is not None:
                    if entry[0] == key:
                        sub_table = entry[1]
                        return sub_table.keys()

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            for entry in self.my_array.array:
                if entry is not None:
                    sub_table = entry[1]
                    for sub_entry in sub_table.array.array:
                        if sub_entry is not None:
                            yield sub_entry[1]
        else:
            top_level_index = self.hash1(key)
            top_level_table_entry = self.my_array.array[top_level_index]
            if top_level_table_entry is not None and top_level_table_entry[0] == key:
                sub_table = top_level_table_entry[1]
                for entry in sub_table.array.array:
                    if entry is not None:
                        yield entry[1]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        return list(self.iter_values(key))

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        top_level_index, sub_table_index = self._linear_probe(key[0], key[1], False)
        return self.my_array.array[top_level_index][1].array[sub_table_index][1]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        top_level_index, sub_table_index = self._linear_probe(key[0], key[1], True) # as this returns top_level_index, sub_table_index
        top_level_entry = self.my_array.array[top_level_index]
        sub_table = top_level_entry[1]
        sub_table[key[1]] = data

        if self.count > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        top_level_index, sub_table_index = self._linear_probe(key[0], key[1], False)
        top_level_entry = self.my_array.array[top_level_index]

        if top_level_entry is not None:
            sub_table = top_level_entry[1]
            try:
                del sub_table[key[1]]  # Try to delete the key from the sub-table
                if len(sub_table) == 0:
                    # If the sub-table is empty, remove the top-level entry
                    self.my_array.array[top_level_index] = None
                    self.count -= 1
                    # Check if this was the last key1 in the table
                    if not any(entry for entry in self.my_array.array):
                        # If there are no other key1 elements, clear out the internal table
                        self.my_array.array = [None] * self.table_size
            except KeyError:
                raise KeyError(key)  # The sub-key doesn't exist
        else:
            raise KeyError(key)  # The top-level key doesn't exist

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)"""

        # Determine the new table size
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # Cannot be resized further.
            return

        # Create a new hash table with the new size
        old_top_array = self.my_array.array
        # Reset the count to 0 as we are starting with an empty table
        self.count = 0
        self.my_array: ArrayR[tuple[K1 | K2, V]] = ArrayR(self.TABLE_SIZES[self.size_index])

        # Rehash and reinsert existing key-value pairs into the new table
        for top_level_entry in old_top_array:
            if top_level_entry is not None:
                key1 = top_level_entry[0]
                sub_table = top_level_entry[1]

                for sub_table_entry in sub_table.array.array:
                    if sub_table_entry is not None:
                        key2 = sub_table_entry[0]
                        value = sub_table_entry[1]

                        # Reinsert the key-value pair into the new sub-table
                        self[key1, key2] = value

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for top_level_entry in self.my_array.array:
            if top_level_entry is not None:
                key1 = top_level_entry[0]
                sub_table = top_level_entry[1]
                for sub_table_entry in sub_table.my_array.array:
                    if sub_table_entry is not None:
                        key2 = sub_table_entry[0]
                        value = sub_table_entry[1]
                        result += f"({key1}, {key2}): {value}\n"
        return result
