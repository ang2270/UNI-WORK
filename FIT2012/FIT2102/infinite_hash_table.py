from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.count = 0
        self.table = ArrayR(self.TABLE_SIZE)
        self.level = 0
        self.positions = []

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        """TIME COMPLEXITY: Worst case: O(N) where n is the length of the key/depth of hash table.
           Best Case is O(1) """
        positions = self.get_location(key)
        current = self.table
        positions.reverse()
        for _ in range(len(positions) - 1):
            index = positions.pop()
            next = current[index]
            current = next[1]

        index = positions.pop()
        return current[index][1]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        """TIME COMPLEXITY: Worst case O(N) where n is the length of the key (and corrosponding depth of hash table), best case O(1)"""
        self.level = 0
        self.set_item_recursive(key, value, self.table)

    def set_item_recursive(self, key: K, value: V, current_table: ArrayR) -> None:
        position = self.hash(key)
        if current_table[position] is None: # Base case 1:
            current_table[position] = (key, value)
            self.count += 1
            return None
        elif current_table[position][0] == key: # Base case 2:
            current_table[position] = (key, value)
            return
        else: # we have a conflict :0
            if not isinstance(current_table[position][1], ArrayR):
                new_array = ArrayR(self.TABLE_SIZE) # new "hash_table"
                old_key, old_value  = current_table[position] # store previously there
                current_table[position] = (key[self.level], new_array) # position for get.item, array for new hash
                self.level += 1
                old_hash = self.hash(old_key)
                new_array[old_hash] = (old_key, old_value)
                current_table = current_table[position][1]
                self.set_item_recursive(key,value,current_table)
            else:
                current_table = current_table[position][1]
                self.level += 1
                self.set_item_recursive(key,value,current_table)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        """TIME COMPLEXITY Worst case O(N) where n is the lenght of the key, best case O(1)"""
        positions = self.get_location(key)
        current = self.table
        positions.reverse()
        level = 0
        self.__delitem_aux(positions, current, key, level)
    def __delitem_aux(self, positions, current, key, level):
        index = positions.pop()
        check = current[index]
        if check[0] == key:
            current[index] = None
            self.count -= 1
        elif key[level] == check[0][0]:
            level += 1
            current = check[1]
            return self.__delitem_aux(positions,current,key,level)
        else:
            raise KeyError(key)
        count = 0
        for i in range(len(current)):
            if current[i] is not None:
                count += 1
                keep_index = i
        if count == 1 and not isinstance(current[keep_index][1], ArrayR):
            keep = current[keep_index]
            current[keep_index] = None
            return keep



    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for list in self.table:
            if list is not None:
                first = True
                for item in list:
                    if not first:
                        result += ' -> '
                    (self.key, self.value) = item
                    result += "(" + str(self.key) + "," + str(self.value) + ")"
                    first = False
                result += '\n'
        return result

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        """Time Complexity: Best case O(1), Worst case O(N) where n is the lenght of the key"""
        self.level = 0
        positions = []
        position = self.hash(key)
        if self.table[position] is None:
            raise KeyError(key)
        if not isinstance(self.table[position][1], ArrayR):
            if self.table[position][0] == key:
                positions.append(position)
                return positions
            else:
                raise KeyError(key)
        else:
            positions.append(self.hash(self.table[position][0]))
            current_table = self.table
            return self.get_location_aux(key, current_table, position, positions)

    def get_location_aux(self, key, current_table, position, positions):
        # if called at current_table[position][1] is an array, therefor we need to go one level deeper
        self.level += 1
        current_table = current_table[position][1] # we go deeper
        position = self.hash(key)
        if current_table[position] is None:
            raise KeyError(key)
        if not isinstance(current_table[position][1], ArrayR):  # Base Case: We arrived at the deepest level
            if current_table[position][0] == key:
                positions.append(position)
                return positions
            else:
                raise KeyError(key)
        else:
            positions.append(position)
            return self.get_location_aux(key,current_table,position,positions)

    def __contains__(self, key: K) -> bool:
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

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        """TIME COMPLEXITY: O(N*LogN)"""
        if current is None:
            current = []

        for item in self.table:
            if item is not None:
                current.append(item[0])

        return current
