from linked_stack import LinkedStack
from random_gen import RandomGen
from hash_table import LinearProbePotionTable
from potion import Potion
from avl import AVLTree

""" 
Main game that stimulates the playing process of trading with vendor and selling
to the adventurer

"""
class Game:
    """
    REASON FOR USED ADTs
        potion_table : Hash Table
            Hash tables, have a search time complexity of O(1) i.e constant in the
            best case and O(n) in the worst case (if implemented properly, it will
            usually always be constant). To minimise our searching time, we have
            chosen a hash table for potion_table

        inventory : AVL Tree
            AVL tree has a search, deletion, and insertion time complexity of
            O(log(N)) in the worst and O(1) in the best case, when the tree is empty.
            To match our required time complexity for the all the used operations (when
            finding the correct potion), we decided to go with the AVL tree.

        ratio tree: AVL Tree
            Used to store the potions in potion_valuation by its profit ratio as
            the key. This allows the tree to be sorted by the best ratio to the worst ratio so
            that when traversing through, it is at its best time complexity to find the best ratio
            to begin the trading and selling process.

            tree stack: Linked Stack
            This stores any duplicates of the same ratio within itself before being
            inserted into the tree. Having this stack allows for any duplication errors to be overcome
            and its implementation to allow for poping and pushing of duplicates when necessary without
            affecting the time complexity of having to iterate through a list or array.
    """

    def __init__(self, seed=0) -> None:
        self.rand = RandomGen(seed=seed)
        self.potion_table = None
        self.inventory = AVLTree()

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        Accepts a list containing potion data and creates empty potion objects
        using that data and adds it to a hash table

        :param potion_data: list of potion data ["Potion of Health Regeneration", "Health", 20]
        :pre: List has to be correct, is not empty
        :complexity: O(N) -> N is the length of potion data
                     adding items to a hash table is O(1)
        :return: None
        """
        self.potion_table = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            name, _type, price = potion
            self.potion_table[name] = Potion.create_empty(_type, name, price)

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Add litres of potion into the current inventory of the vendor company. Takes a list
        of tuples containing names of potion and a float representing litres to add to the inventory.
        :raises ValueError: if current is None, raises Subtree is empty
        :complexity: Best O(1) if subtree is empty, worst O(log N) where N is the height
                        of current.
        """
        for potion in potion_name_amount_pairs:
            name, amount = potion
            potion_object = self.potion_table[name]
            potion_object.quantity = amount
            self.inventory[potion_object.buy_price] = (potion_object, amount)

    def choose_potions_for_vendors(self, num_vendors: int) -> list[tuple[str, float]]:
        """
        This method completes the vendor potion selection process and returns a list
        of potion names along with their quantity in inventory
        :param num_vendors: int
        :pre: num_vendors > 0
        :required complexity: O(C x log(N))
        :achieved complexity: O(C x log(N))
        :return: list of tuples [(name_of_potion, quantity)]
        """
        # self.inventory.print_tree()
        vendor_potion_list = []
        checked = [0]
        # saved_inventory = self.inventory
        # O(C) -> C is the number of vendors
        for i in range(num_vendors):
            p = 0
            while p in checked:
                p = self.rand.randint(len(self.inventory))
            checked.append(p)
            pth_index = (len(self.inventory) - p)
            # O(log(N)) -> N is the number of items in inventory
            for j, key in list(enumerate(self.inventory)):
                # p starts from 1 - k, hence we add 1 to j
                if pth_index == j:
                    # getting items from an AVL tree is usually O(1)
                    node = self.inventory.get_tree_node_by_key(key).item
                    name, amount = node[0].name, node[1]
                    self.potion_table[name].quantity = amount
                    vendor_potion_list.append((name, amount))
                    # del self.inventory[key]
                    break

        # self.inventory = saved_inventory
        return vendor_potion_list

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        Uses the starting money to buy and sell potions for the amount of money left at the
        end of each played day.

        :param arg1: potion_valuations: is a list of potions that each vendor is selling, paired with its valuation
                           by the adventurers
        :param arg2: starting_money: is a list containing, for each attempt, the starting allowance the player has.
        :pre: potion_valuations is not empty, and is a list of tuple[str, float], starting money is a list of ints
        :raises ValueError: if potion_valuations is empty

        :complexity best case: 𝐎(𝑁 + 𝑀) - where the O(N) is the n length of
            the potion_valuation that is being iterated through. The best case
            complexity for insertion and searcg a binary search tree is O(1)
            where the tree is empty or the searching key is at the tree root.
        :complexity worst case: 𝐎(𝑁 x log(N) + 𝑀 × N) - the O(N) for the n length of potion_valuation remains
            the same but the insertion into the BST becomes log(N) where the tree is balanced and sorted
            so the given key can be found by comparing keys. This is the same complexity for searching
            where the tree is sorted and balanced
        """

        day_profits = []
        ratio_tree = AVLTree()
        try:
            if len(potion_valuations) == 0:
                raise ValueError(f"List has length: {len(potion_valuations)}")
            if len(starting_money) == 0:
                raise ValueError("List has length 0")
        except Exception as e:
            print(f"Error: {type(e)}: {e}")
            return day_profits
        """
        This for loop goes through each potion_valuation and creates the binary tree.
        
        :pre: this list of potion_valuation must contain 1 or more elements
        :raises ValueError: if the list is empty
        
        This solution requires for each value of the potion_valuation have a profit 
        ratio calculated. This is then used as its key to be inserted into a sorted 
        AVL tree as a tuple with a boolean value. To solve the issue of duplicates, 
        if the tree contains the key already, it simply changes the boolean in the 
        tuple to True and creates a stack to store each potion with the same key.
        """

        for i in range(len(potion_valuations)):

            name, valuation = potion_valuations[i] # splitting potion_valuation by line
            vendor_buy_price = self.potion_table[name].buy_price
            profit_margin = valuation - vendor_buy_price
            ratio = profit_margin / vendor_buy_price  # profit ratio using the name from the hash table
            quantity = self.potion_table[name].quantity

            if ratio not in ratio_tree:     # checks if the key ratio already exists
                ratio_tree[ratio] = (False, (name, vendor_buy_price, valuation, profit_margin, ratio, quantity))      # if key node is empty, add a tuple with False and the potion details
            else:
                tree_stack = LinkedStack()      # if duplicate exists, create linked stack
                current_potion = ratio_tree[ratio][1] # save the current potion details in that key
                del ratio_tree[ratio]       # delete the key to avoid duplicate error
                tree_stack.push(current_potion)     # push the current potion into the empty stack
                tree_stack.push((name, vendor_buy_price, valuation, profit_margin, ratio, quantity))    # push the new potion into the stack
                ratio_tree[ratio] = (True, tree_stack)      # insert the tuple of True and stack to indicate it is a duplicate

        """
            Iterates through the money values for each day and calculates the money remaining 
            at the end of each iteration(day)
            :pre: the tree must exist and its root must not be None
            :raises Exception: if the tree does not exist
            :pre: there must be integer values in starting_money list
            :raises Exception: if the list has not been defined
        """
        try:
            if ratio_tree.root is None:
                raise TypeError("Ratio tree does not exist")
        except Exception as e:
            print(f"Error: {type(e)}: {e}")
            return day_profits

        for money in starting_money:    # Loop Time complexity: O(M)

            checked = []
            temp_stack = LinkedStack()
            final_money = 0
            print(f"\nStaring Day Money: {money}")

            while money > 0 and len(checked) <= len(ratio_tree):
                max_ratio = ratio_tree.get_minimal(ratio_tree.root).key
                # loops through the ratio tree for the maximum ratio and extracts it from the tree
                for ratio in ratio_tree:
                    if ratio >= max_ratio and not (ratio in checked):
                        max_ratio = ratio
                best_ratio_item = ratio_tree[max_ratio]

                # Checks the number to see if its first element is true. This means it's a duplicate
                # and it will then store the stack and pop off its first element. In doing so it also
                # pushes this popped element into the temp_stack. If False then continues to store the
                # potion tuple and add its ratio to the checked list.
                if best_ratio_item[0]:
                    original_stack = best_ratio_item[1]
                    item = original_stack.pop()
                    temp_stack.push(item)

                    # checks after popping, if the stack is empty. Adds the ratio to the checked list
                    # and deletes the redundant node at that key with the empty stack before readding
                    # it with the full temp_stack
                    if original_stack.is_empty():
                        checked.append(max_ratio)
                        del ratio_tree[max_ratio]
                        ratio_tree[max_ratio] = (True, temp_stack)
                else:
                    checked.append(max_ratio)
                    item = best_ratio_item[1]

                print(f"Potion bought: {item}")
                name, vendor_buy_price, valuation, profit_margin, ratio, quantity = item  # split item into its parts

                # checks if there is money remaining after buying the whole inventory of that potion.
                # calculates the profit for the day and subtracts the money lost from the total money.
                # else it will see how much was bought and calculate the new profit before making money
                # equal 0
                if money >= quantity * vendor_buy_price:
                    final_money += quantity * valuation
                    print(f"Bought the whole stock: {quantity}L for ${vendor_buy_price} each\n")
                    money -= quantity * vendor_buy_price
                    print(f"Money left: {money}")
                else:
                    new_quantity = money / vendor_buy_price
                    print(f"Went broke buying: {new_quantity}L for ${vendor_buy_price} each\n")
                    final_money += new_quantity * valuation
                    money = 0

            day_profits.append(final_money)

        return day_profits
