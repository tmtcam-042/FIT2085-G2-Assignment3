from __future__ import annotations
# ^ In case you aren't on Python 3.10
from linked_stack import LinkedStack
from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from avl import AVLTree
from array_list import ArrayList
from stack_adt import Stack
from linked_list import LinkedList


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
        ratio_tree = AVLTree()

        # creating the tree
        for i in range(len(potion_valuations)):
            name, valuation = potion_valuations[i]
            current_potion = self.potion_table[name]
            vendor_buy_price, quantity = current_potion.buy_price, current_potion.quantity
            profit_margin = (valuation - vendor_buy_price) / valuation
            if profit_margin not in ratio_tree:
                ratio_tree[profit_margin] = LinkedList()
            insert_index = len(ratio_tree[profit_margin])
            ratio_tree[profit_margin].insert(insert_index, (name, vendor_buy_price, valuation, profit_margin, quantity))

        # iterating through the days
        for day, money in enumerate(starting_money):
            profit_for_the_day = 0
            visited_items = []
            visited_nodes = []

            while money >= 0:
                max_ratio = 0
                for ratio in ratio_tree:  # O(N)
                    if ratio > max_ratio and ratio not in visited_nodes:
                        max_ratio = ratio
                most_valuable_items = ratio_tree[max_ratio]
                most_valuable_item = most_valuable_items[0]
                for i in range(len(most_valuable_items)):
                    if most_valuable_items[i][1] > most_valuable_item[1] and \
                            most_valuable_items[i] not in visited_items:
                        most_valuable_item = most_valuable_item[i]

                # most valuable item details
                name, vendor_buy_price, valuation, profit_margin, quantity = most_valuable_item
                # potion amount > money -> money finishes
                if quantity * valuation >= money:
                    profit_for_the_day += (money/valuation)*vendor_buy_price
                    break
                # money > potion amount -> potion finishes
                else:
                    profit_for_the_day += quantity * valuation
                    # profit_for_the_day += (quantity * valuation) - (quantity * vendor_buy_price)
                    money -= quantity * valuation
                    visited_items.append(most_valuable_item)
                    all_items_in_visited = all(elem in most_valuable_items for elem in visited_items)
                    if all_items_in_visited:
                        visited_nodes.append(profit_margin)

            day_profits.append(profit_for_the_day)

        # =================================

        # for i in range(len(potion_valuations)):  # O(N)
        #     name, valuation = potion_valuations[i]
        #     vendor_buy_price = self.potion_table[name].buy_price
        #     profit_margin = valuation - vendor_buy_price
        #     ratio = profit_margin / valuation
        #     quantity = self.potion_table[name].quantity
        #     print(f"Quantity: {quantity}")
        #     # assuming normal potions
        #     if ratio not in ratio_tree:
        #         tree_stack = LinkedStack()
        #         tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
        #         ratio_tree[ratio] = tree_stack
        #     else:
        #         tree_stack = ratio_tree[ratio]
        #         del ratio_tree[ratio]
        #         tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
        #         ratio_tree[ratio] = tree_stack
        #
        # for money in starting_money:  # O(M)
        #     profit_for_day = 0
        #     while money > 0:
        #         max_ratio = 0
        #         for ratio in ratio_tree:  # O(N)
        #             if ratio > max_ratio:
        #                 max_ratio = ratio
        #
        #         # check is the current ratio is in the duplicate list
        #         best_ratio_item = ratio_tree[max_ratio]
        #         item = best_ratio_item.pop()
        #         name, vendor_buy_price, valuation, profit_margin, ratio, quantity = item
        #         # when we can buy all of the potion. -> Potion finishes
        #         if money >= quantity * vendor_buy_price:
        #             profit_for_day += quantity * valuation  # Money earned from sale of potion
        #             money -= quantity * vendor_buy_price  # Available money is reduced
        #             if best_ratio_item.is_empty():
        #                 del ratio_tree[max_ratio]
        #         else:
        #             # we spend all our money buying the potions
        #             # (which is available in sufficient quantity) -> Money Finishes
        #             new_quantity = money / vendor_buy_price  # quantity of potion purchased (L)
        #             profit_for_day += new_quantity * valuation  # money earned from sale of potion
        #             money = 0
        #
        #     print(f"DAY PROFIT RATIO: {profit_for_day}")

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
