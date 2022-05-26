from __future__ import annotations
# ^ In case you aren't on Python 3.10

from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from bst import BinarySearchTree


class Game:

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.potion_table = None
        self.inventory = BinarySearchTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        """ Hash table!

        :param potion_data:
        :pre: List has to be correct, is not empty
        :return:
        """
        self.potion_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            name, _type, price = potion
            self.potion_table[name] = Potion.create_empty(_type, name, price)
            print(self.potion_table)

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Binary tree!
        :param potion_name_amount_pairs:
        :return:
        :complexity: worst case = constant comparison * depth
        """
        for potion in potion_name_amount_pairs:
            name, amount = potion
            potion_object = self.potion_table[name]
            self.inventory[potion_object.buy_price] = (potion_object, amount)
        self.inventory.draw()

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """

        """
        vendor_potion_list = []
        for i in range(num_vendors):
            p = self.rand.randint(len(self.potion_table))
            minimal = self.inventory.get_minimal(self.inventory.root)

            # successor = None
            # for j in range(p):
            #     successor = self.inventory.get_successor(minimal)
            #
            # if successor is not None:
            #     name = successor.item(0).name
            #     amount = successor.item(1)
            #     vendor_potion_list.append((name, amount))

            for j, key in enumerate(self.inventory):
                if p == j:
                    name = self.inventory.get_tree_node_by_key(key).item[0].name
                    amount = self.inventory.get_tree_node_by_key(key).item[1]
                    vendor_potion_list.append((name, amount))
                    break

        return vendor_potion_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        raise NotImplementedError()
