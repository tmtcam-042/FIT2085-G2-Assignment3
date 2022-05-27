from __future__ import annotations
# ^ In case you aren't on Python 3.10

from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from bst import BinarySearchTree
from array_list import ArrayList


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
        self.inventory.print_tree()
        vendor_potion_list = []
        saved_inventory = self.inventory
        for i in range(num_vendors):
            p = self.rand.randint(len(self.inventory))

            for j, key in enumerate(self.inventory):
                # p starts from 1 - k, hence we add 1 to j
                if p == j + 1:
                    node = self.inventory.get_tree_node_by_key(key).item
                    name, amount = node[0].name, node[1]
                    self.potion_table[name].quantity = amount
                    vendor_potion_list.append((name, amount))
                    del self.inventory[key]
                    break

        self.inventory = saved_inventory
        self.inventory.print_tree()
        return vendor_potion_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        potion_valuations: is a list of potions that each vendor is selling, paired with its valuation
                           by the adventurers
        starting_money: is a list containing, for each attempt, the starting allowance the player has.

        required complexity: 𝐎(𝑁 × log(𝑁) + 𝑀 × 𝑁)
        """
        # profit = self.potion_table[2] - potion_valuations[i][1]
        day_profits = []
        # profit_margins = {}
        # # Calculating profit margins
        # for i in range(len(potion_valuations)):
        #     name, valuation = potion_valuations[i]
        #     profit_margin = valuation - self.potion_table[name].buy_price
        #     quantity = self.potion_table[name].quantity
        #     vendor_buy_price = self.potion_table[name].buy_price
        #     profit_margins[name] = (profit_margin, quantity, vendor_buy_price)

        # for potion_info in potion_valuations:
        #     name, price = potion_info
        #     buy_price = self.potion_table[name].buy_price
        #     quantity = self.potion_table[name].quantity
        #     print(f"Name: {name}, buy_price: {buy_price} Quantity: {quantity}")
        #     for money in starting_money:
        #         pass

        # ===========================================================
        # current_highest_margin = 0
        # for key, value in profit_margins.items():
        #     profit_margin, quantity, buy_price = value
        #
        #     if current_highest_margin <= profit_margin:
        #         current_highest_margin = profit_margin
        #         cheapest_potion.append(key)

        profit_ratio = BinarySearchTree()

        # profit_ratio = ArrayList(len(potion_valuations))
        for i in range(len(potion_valuations)):
            name, valuation = potion_valuations[i]
            vendor_buy_price = self.potion_table[name].buy_price
            profit_margin = valuation - vendor_buy_price
            ratio = profit_margin/vendor_buy_price
            quantity = self.potion_table[name].quantity
            profit_ratio[ratio] = (name, vendor_buy_price, valuation, profit_margin, quantity)


        for money in starting_money:
            max_ratio = 0
            for ratio in profit_ratio:
                if ratio > max_ratio:
                    max_ratio = ratio
            best_ratio_item = profit_ratio.get_minimal(profit_ratio.root)



            index_of_max_ratio = profit_ratio.index(max_ratio)
            potion_details = potion_valuations[index_of_max_ratio]
            name = self.potion_table[potion_details[0]].name
            quantity = self.potion_table[potion_details[0]].quantity

            bought_quantity =
            print(name, quantity)



        print(f"HELLOWW!: {cheapest_potion}")
        # for money in starting_money:

        return day_profits
