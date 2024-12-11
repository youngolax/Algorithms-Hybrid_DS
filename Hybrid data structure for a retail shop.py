class Node:
    """
    Represents a single node in the Binary Search Tree (BST).
    Each node contains a key (product ID), value (product details), and pointers to left and right children.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class RetailShopHybrid:
    """
    A hybrid data structure combining a Hash Table for fast lookups and a BST for maintaining sorted order.
    """
    def __init__(self):
        self.hash_table = {}  # Hash Table for O(1) average-case lookups
        self.root = None  # Root of the BST

    def _insert_bst(self, node, key, value):
        """
        Helper function to recursively insert a key-value pair into the BST.
        """
        if not node:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert_bst(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_bst(node.right, key, value)
        return node

    def insert(self, key, value):
        """
        Inserts a product record into both the Hash Table and the BST.
        Args:
            key: The product ID (unique).
            value: The product details (e.g., name, price, stock).
        """
        self.hash_table[key] = value  # Insert into Hash Table
        self.root = self._insert_bst(self.root, key, value)  # Insert into BST

    def _search_bst(self, node, key):
        """
        Helper function to recursively search for a key in the BST.
        """
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search_bst(node.left, key)
        return self._search_bst(node.right, key)

    def search(self, key):
        """
        Searches for a product by its ID in the hybrid structure.
        Args:
            key: The product ID to search for.
        Returns:
            The product details if found, otherwise None.
        """
        # Check in the Hash Table first
        if key in self.hash_table:
            return self.hash_table[key]
        # Fallback to BST search
        bst_node = self._search_bst(self.root, key)
        return bst_node.value if bst_node else None

    def _delete_bst(self, node, key):
        """
        Helper function to recursively delete a key-value pair from the BST.
        """
        if not node:
            return node
        if key < node.key:
            node.left = self._delete_bst(node.left, key)
        elif key > node.key:
            node.right = self._delete_bst(node.right, key)
        else:
            # Node with one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Node with two children: Get the inorder successor
            temp = self._min_value_node(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete_bst(node.right, temp.key)
        return node

    def delete(self, key):
        """
        Deletes a product record by its ID from both the Hash Table and the BST.
        Args:
            key: The product ID to delete.
        """
        # Remove from Hash Table
        if key in self.hash_table:
            del self.hash_table[key]
        # Remove from BST
        self.root = self._delete_bst(self.root, key)

    def _min_value_node(self, node):
        """
        Helper function to find the node with the smallest key in the BST (inorder successor).
        """
        current = node
        while current.left:
            current = current.left
        return current

    def in_order_traversal(self, node):
        """
        Performs an in-order traversal of the BST and prints all key-value pairs.
        """
        if node:
            self.in_order_traversal(node.left)
            print(f"Product ID: {node.key}, Details: {node.value}")
            self.in_order_traversal(node.right)

    def print_sorted_products(self):
        """
        Prints all product records in sorted order by their IDs using the BST.
        """
        self.in_order_traversal(self.root)


# Example Usage
retail_shop = RetailShopHybrid()

# Insert product records
retail_shop.insert(101, {"name": "Laptop", "price": 1500, "stock": 10})
retail_shop.insert(102, {"name": "Phone", "price": 800, "stock": 20})
retail_shop.insert(103, {"name": "Tablet", "price": 500, "stock": 15})

# Search for products
print("Searching for Product ID 102:")
print(retail_shop.search(102))  # Should return product details for ID 102

print("\nSearching for Product ID 200:")
print(retail_shop.search(200))  # Should return None (not found)

# Print all products in sorted order by ID
print("\nProducts in sorted order:")
retail_shop.print_sorted_products()

# Delete a product
print("\nDeleting Product ID 102...")
retail_shop.delete(102)

# Verify deletion
print("\nAfter deletion, products in sorted order:")
retail_shop.print_sorted_products()
