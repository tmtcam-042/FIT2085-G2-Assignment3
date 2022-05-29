from linked_stack import LinkedStack
from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from avl import AVLTree


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

    def choose_potions_for_vendors(self, num_vendors: int) -> list:
        """

        """
        # self.inventory.print_tree()
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
        return vendor_potion_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        Uses the starting money to buy and sell potions for the amount of money left at the
        end of each played day.

        :param arg1: potion_valuations: is a list of potions that each vendor is selling, paired with its valuation
                           by the adventurers
        :param arg2: starting_money: is a list containing, for each attempt, the starting allowance the player has.

        :complexity best case: 𝐎(𝑁 × log(𝑁) + 𝑀 × log(N))
        :complexity worst case: 𝐎(𝑁^2 + 𝑀 × N)
        :average complexity: 𝐎(𝑁 × log(𝑁) + 𝑀 × 𝑁)
        """

        day_profits = []
        ratio_tree = AVLTree()

        """
        This for loop goes through each potion_valuation and creates the binary tree.
        :pre: this list of potion_valuation must contain 1 or more elements
        :raises ValueError: if the list is empty
        :complexity best: O(N) x O(log(N)) - where the O(N) is the n length of 
        the potion_valuation that is being iterated through. The best case 
        complexity for insertion in a BST is log(N) where the tree is balanced
        :complexity worst: O(N^2) - the O(N) for the n length of potion_valuation remains
        the same but the insertion
        :average complexity: O(N) x O(log(N))
        """
        # TODO: CHECK THIS IS RIGHT AND GET RID OF PRINT STATEMENTS
        for i in range(len(potion_valuations)): # Loop time complexity: O(N) where N is the length of potion_valuations

            if len(potion_valuations) == 0:
                raise ValueError(f"List has length: {len(potion_valuations)}")

            name, valuation = potion_valuations[i]
            vendor_buy_price = self.potion_table[name].buy_price
            profit_margin = valuation - vendor_buy_price
            ratio = profit_margin / vendor_buy_price
            quantity = self.potion_table[name].quantity

            if ratio not in ratio_tree:     # Binary Tree Insertion Time complexity: O(log(N))
                ratio_tree[ratio] = (False, (name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
            else:
                tree_stack = LinkedStack()
                dup_ratio = ratio_tree[ratio][1]
                del ratio_tree[ratio]
                tree_stack.push(dup_ratio)
                tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))
                ratio_tree[ratio] = (True, tree_stack)

        """
            Iterates through the money values for each day and calculates the money remaining 
            at the end of each iteration(day)
            
            :pre: the tree must exist and its root must not be None
            :raises Exception: if the tree does not exist
            :pre: there must be integer values in starting_money list
            :raises Exception: if the list has not been defined
            :complexity best: O(M) x O(log(N))
            :complexity worst: O(M) x O(N)
            :average complexity: O(M) x O(N)
        """
        for money in starting_money:    # Loop Time complexity: O(M)

            if ratio_tree.root is None:
                raise TypeError("Ratio tree does not exist")
            elif len(starting_money) == 0:
                raise ValueError("List has length 0")

            checked = []
            temporary_stack = LinkedStack()
            profit_for_day = 0
            print(f"\nStaring Day Money: {money}")

            while money > 0:
                max_ratio = ratio_tree.get_minimal(ratio_tree.root).key
                for ratio in ratio_tree:  # Loop Time complexity: O(N)
                    if ratio >= max_ratio and not (ratio in checked):
                        max_ratio = ratio

                best_ratio_item = ratio_tree[max_ratio]
                original_stack = best_ratio_item[1]

                if best_ratio_item[0]:  # checks is the stack is True (duplicate)
                    item = original_stack.pop()  # pops it off
                    temporary_stack.push(item)  # pushes it into the temporary stack

                    if original_stack.is_empty():  # if the stack is empty (no more duplicates)
                        checked.append(max_ratio)  # add the node to visited nodes
                        del ratio_tree[max_ratio]  # delete the node at that key
                        ratio_tree[max_ratio] = (True, temporary_stack) # reset it by putting the temp stack in place of the whole stack
                else:
                    checked.append(max_ratio)  # if no duplicate, add key to checked list
                    item = best_ratio_item[1]  # item is the second element bc there is no stack

                print(f"Potion bought: {item}")
                name, vendor_buy_price, valuation, profit_margin, ratio, quantity = item  # split item into its parts

                if money >= quantity * vendor_buy_price:  # if we can buy the whole inventory and still have money left
                    profit_for_day += quantity * valuation  # whole inventory * adventurer buy price
                    print(f"Bought the whole stock: {quantity}L for ${vendor_buy_price} each\n")
                    money -= quantity * vendor_buy_price  # subtract this from the money
                    print(f"Money left: {money}")
                else:
                    if best_ratio_item[0]:  # if it was a part of a duplicate and it was only the first one used, put it back
                        original_stack.push(item)
                    new_quantity = money / vendor_buy_price  # quantity of potion purchased (L)
                    print(f"Went broke buying: {new_quantity}L for ${vendor_buy_price} each\n")
                    profit_for_day += new_quantity * valuation  # money earned from sale of potion
                    money = 0  # set money to 0 since we broke

            day_profits.append(profit_for_day)

        return day_profits
