from __future__ import annotations

from mountain import Mountain

class TreeNode:
    def __init__(self, mountain: Mountain):
        """
        Initialize a TreeNode with a mountain object.
        """
        self.mountain = mountain
        self.left = None
        self.right = None
        self.left_count = 0  # Number of mountains in the left subtree (including itself)
        self.same_length_mountains = []

class MountainOrganiser:
    def __init__(self):
        """
        Initialize a MountainOrganiser instance with an empty root.
        """
        self.root = None

    def add_mountains(self, mountains):
        """
        Adds a list of mountains to the organizer.
        :complexity: O(logn), O(n) in the worst case where n is the number of mountains in the tree. 
        """
        for mountain in mountains:
            self.root = self._insert(self.root, mountain)

    def _insert(self, node, mountain):
        """
        Insert a mountain into the tree rooted at the given node.
        :complexity: O(logn), O(n) in the worst 
        """
        if node is None:
            return TreeNode(mountain)
        
        if mountain.length < node.mountain.length:
            node.left = self._insert(node.left, mountain)
            node.left_count += 1
        elif mountain.length > node.mountain.length:
            node.right = self._insert(node.right, mountain)
        else:
            # If mountain lengths are equal, add it to the list
            node.same_length_mountains.append(mountain)
        return node

    def cur_position(self, mountain):
        """
        Finds the rank of the provided mountain given all mountains included so far.
        :complexity: O(logn), O(n) in the worst case 
        """
        return self._rank(self.root, mountain)

    def _rank(self, node, mountain):
        """
        Recursively finds the rank of the provided mountain given all mountains included so far.
        :raises KeyError: when the provided mountain hasn't been added yet.
        :complexity: O(logn), O(n) in the worst case 
        """
    
        if node is None:
            raise KeyError("Mountain not found in the organizer")
        
        if mountain.length == node.mountain.length:
            # If lengths are equal, count all same-length mountains in the left subtree
            rank = node.left_count 
            for same_length_mountain in node.same_length_mountains:
                if same_length_mountain != mountain:
                    rank += 1
            return rank
        elif mountain.length < node.mountain.length:
            return self._rank(node.left, mountain)
        else:
            # Increment the rank in the right subtree
            return node.left_count + 1 + self._rank(node.right, mountain) 
