from __future__ import annotations
# ^ In case you aren't on Python 3.10
from linked_stack import LinkedStack
from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from avl import AVLTree
from array_list import ArrayList
from stack_adt import Stack



class Game:

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.potion_table = None
        self.inventory = AVLTree()

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
            self.potion_table[name].quantity = amount
            potion_object = self.potion_table[name]
            self.inventory[potion_object.buy_price] = (potion_object, amount)
        self.inventory.print_tree()

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
                    # self.potion_table[name].quantity = amount
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

        ratio_tree = AVLTree()
        # ratio_tree = ArrayList(len(potion_valuations))
        for i in range(len(potion_valuations)): # O(N)
            name, valuation = potion_valuations[i]
            # print(f"Name: {name}")
            vendor_buy_price = self.potion_table[name].buy_price
            profit_margin = valuation - vendor_buy_price
            ratio = profit_margin / vendor_buy_price
            quantity = self.potion_table[name].quantity
            print(f"Quantity: {quantity}")

            # assuming normal potions
            if ratio not in ratio_tree:
                tree_stack = LinkedStack()
                tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
                ratio_tree[ratio] = tree_stack
            else:
                tree_stack = ratio_tree[ratio]
                del ratio_tree[ratio]
                tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
                ratio_tree[ratio] = tree_stack

        for money in starting_money: # O(M)
            profit_for_day = 0
            while money > 0:
                max_ratio = 0
                for ratio in ratio_tree: # O(N)
                    if ratio > max_ratio:
                        max_ratio = ratio

                # check is the current ratio is in the duplicate list
                best_ratio_item = ratio_tree[max_ratio]
                item = best_ratio_item.pop()
                name, vendor_buy_price, valuation, profit_margin, ratio, quantity = item
                # when we can buy all of the potion. -> Potion finishes
                if money >= quantity * vendor_buy_price:
                    profit_for_day += quantity * valuation  # Money earned from sale of potion
                    money -= quantity * vendor_buy_price # Available money is reduced
                    if best_ratio_item.is_empty():
                        del ratio_tree[max_ratio]
                else:
                    # we spend all our money buying the potions
                    # (which is available in sufficient quantity) -> Money Finishes
                    new_quantity = money / vendor_buy_price  # quantity of potion purchased (L)
                    profit_for_day += new_quantity * valuation # money earned from sale of potion
                    money = 0

            print(f"DAY PROFIT RATIO: {profit_for_day}")

            # if our money exceeds amount of available potion
            # otherwise find next available potion

        #     index_of_max_ratio = ratio_tree.index(max_ratio)
        #     potion_details = potion_valuations[index_of_max_ratio]
        #     name = self.potion_table[potion_details[0]].name
        #     quantity = self.potion_table[potion_details[0]].quantity
        #
        #     bought_quantity =
        #     print(name, quantity)
        #
        #
        #
        # print(f"HELLOWW!: {cheapest_potion}")
        # for money in starting_money:

        return day_profits