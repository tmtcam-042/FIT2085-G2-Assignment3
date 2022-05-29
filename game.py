from typing import List, Tuple

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

    def add_potions_to_inventory(self, potion_name_amount_pairs: List[Tuple[str, float]]) -> None:
        """
        Binary tree!
        :param potion_name_amount_pairs:
        :return:
        :complexity: worst case = constant comparison * depth
        """
        for potion in potion_name_amount_pairs:
            name, amount = potion
            potion_object = self.potion_table[name]
            potion_object.quantity = amount
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
            pth_index = len(self.inventory) - p

            for j, key in reversed(list(enumerate(self.inventory))):
                # p starts from 1 - k, hence we add 1 to j
                if pth_index == j:
                    node = self.inventory.get_tree_node_by_key(key).item
                    name, amount = node[0].name, node[1]
                    self.potion_table[name].quantity = amount
                    vendor_potion_list.append((name, amount))
                    del self.inventory[key]
                    break

        self.inventory = saved_inventory
        self.inventory.print_tree()
        return vendor_potion_list

    def solve_game(self, potion_valuations: List[Tuple[str, float]], starting_money: List[int]) -> List[float]:
        """
        potion_valuations: is a list of potions that each vendor is selling, paired with its valuation
                           by the adventurers
        starting_money: is a list containing, for each attempt, the starting allowance the player has.

        required complexity: 𝐎(𝑁 × log(𝑁) + 𝑀 × 𝑁)
        """
        day_profits = []
        ratio_tree = AVLTree()
        for i in range(len(potion_valuations)):  # O(N)
            name, valuation = potion_valuations[i]
            vendor_buy_price = self.potion_table[name].buy_price
            profit_margin = valuation - vendor_buy_price
            ratio = profit_margin / vendor_buy_price
            quantity = self.potion_table[name].quantity
            print(f"Quantity: {quantity}")

            # assuming normal potions
            if ratio not in ratio_tree:
                ratio_tree[ratio] = (False, (name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
            else:
                tree_stack = LinkedStack()
                dup_ratio = ratio_tree[ratio][1]
                del ratio_tree[ratio]
                tree_stack.push(dup_ratio)
                tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
                ratio_tree[ratio] = (True, tree_stack)

        for money in starting_money:  # O(M)
            checked = []
            dup_checker = []
            profit_for_day = 0
            while money > 0:
                max_ratio = 0
                for ratio in ratio_tree:  # O(N)
                    if ratio > max_ratio and not (ratio in checked):
                        max_ratio = ratio

                # check is the current ratio is in the duplicate list
                best_ratio_item = ratio_tree[max_ratio]
                if best_ratio_item[0]:
                    stack_item = best_ratio_item[1]
                    check_item = stack_item.peek()
                    if check_item[0] not in dup_checker:
                        item = stack_item.peek()
                        dup_checker.append(item[0])
                    else:
                        temp_item = stack_item.pop()
                        item = stack_item.peek()
                        stack_item.push(temp_item)
                else:
                    checked.append(max_ratio)
                    item = best_ratio_item[1]
                print(item)
                name, vendor_buy_price, valuation, profit_margin, ratio, quantity = item
                # when we can buy all of the potion. -> Potion finishes
                if money >= quantity * vendor_buy_price:
                    profit_for_day += quantity * valuation  # Money earned from sale of potion
                    print(quantity)
                    money -= quantity * vendor_buy_price  # Available money is reduced
                else:
                    # we spend all our money buying the potions
                    # (which is available in sufficient quantity) -> Money Finishes
                    new_quantity = money / vendor_buy_price  # quantity of potion purchased (L)
                    print(new_quantity)
                    profit_for_day += new_quantity * valuation  # money earned from sale of potion
                    money = 0

            day_profits.append(profit_for_day)

        return day_profits
