""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
"""
__author__ = 'Brendon Taylor, modified by Jackson Goerner'
__docformat__ = 'reStructuredText'
__modified__ = '21/05/2020'
__since__ = '14/05/2020'

from potion import Potion
from referential_array import ArrayR
from typing import TypeVar, Generic

T = TypeVar('T')


class LinearProbePotionTable(Generic[T]):
    """
    Linear Probe Potion Table

    This potion table does not support deletion.

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        table_size: current size of the hash table
    """

    def __init__(self, max_potions: int, good_hash: bool = True, tablesize_override: int = -1) -> None:
        # Statistic setting
        self.conflict_count = 0
        self.probe_max = 0
        self.probe_total = 0

        self.count = 0
        self.table = None
        self.table_size = 0

        self.useHash = False

        if tablesize_override != -1:
            self.initalise_with_tablesize(tablesize_override)
        else:
            self.initalise_with_tablesize(max_potions * 2)

        if good_hash:
            self.useHash = True

    def hash(self, potion_name: str) -> int:
        """
        Hashes the potions name
        """
        if self.useHash:
            return Potion.good_hash(potion_name, self.table_size)  # added a getter to the Potion class, unsure if this works
        else:
            return Potion.bad_hash(potion_name, self.table_size)

    def statistics(self) -> tuple:
        """"""
        stat_tuple = (self.conflict_count, self.probe_total, self.probe_max,)
        return stat_tuple

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self.count

    def __linear_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing
        :complexity best: O(K) first position is empty
                          where K is the size of the key
        :complexity worst: O(K + N) when we've searched the entire table
                           where N is the table_size
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash i = 2

        if is_insert and self.is_full():
            raise KeyError(key)

        probe_chain = []
        conflict_check = 0
        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                self.conflict_count += conflict_check
                if self.probe_max < len(probe_chain):
                    self.probe_max = len(probe_chain)
                if is_insert: # trying to insert (bool)
                    return position # returns the position of empty slot
                else: # not trying to insert (search)
                    raise KeyError(key)  # so the key is not in the table (search function)
            elif self.table[position][0] == key:  # found key (search function)
                return position # return
            else:  # there is something but not the key, try next (inserting item)
                if conflict_check == 0:
                    conflict_check = 1
                probe_chain.append(position)
                position = (position + 1) % len(self.table)  # next index
                self.probe_total += 1

        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist
        """
        position = self.__linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set an (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__contains__(key: str)
        """
        if len(self) == len(self.table) and key not in self:
            raise ValueError("Cannot insert into a full table.")
        position = self.__linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)

    def initalise_with_tablesize(self, tablesize: int) -> None:
        """
        Initialise a new array, with table size given by tablesize.
        Complexity: O(n), where n is len(tablesize)
        """
        self.count = 0
        self.table_size = tablesize
        self.table = ArrayR(tablesize)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
