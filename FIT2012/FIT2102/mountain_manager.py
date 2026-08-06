from __future__ import annotations
from mountain import Mountain


class MountainManager:

    def __init__(self) -> None:
        """
        Initialize a new MountainManager instance with an empty list of mountains. 
        """
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Add a mountain to the list of mountains.
        :complexity: O(1) 
        """
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Remove a specified mountain from the list.
        :complexity: O(n) where n is the number of mountains in the list 
        """
        
        if mountain in self.mountains:
            self.mountains.remove(mountain)

    def edit_mountain(self, old_mountain: Mountain, new_mountain: Mountain) -> None:
        """
        Edit a mountain in the list by replacing the old mountain with a new one.
        :complexity: O(n) where n is the number mountains in the list 
        """
        if old_mountain in self.mountains:
            self.mountains.remove(old_mountain)
        self.mountains.append(new_mountain)

    def mountains_with_difficulty(self, diff: str) -> list[Mountain]:
        """
        Get a list of mountains with the specified difficulty level.
        :complexity: O(n) where n is the number of mountains in the list 
        """
        return [mountain for mountain in self.mountains if mountain.difficulty_level == diff]

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Group mountains by difficulty level and return them in ascending order of difficulty.
        :complexity: O(nlogn) where n is the number of mountains in the list 
        """
        grouped_mountains = {}
        for mountain in self.mountains:
            diff = mountain.difficulty_level 
            if diff in grouped_mountains:
                grouped_mountains[diff].append(mountain)
            else:
                grouped_mountains[diff] = [mountain]

        # Sort the grouped mountains by difficulty in ascending order
        sorted_grouped_mountains = sorted(grouped_mountains.items())

        # Extract the sorted lists of mountains
        result = [mountains for diff, mountains in sorted_grouped_mountains]

        return result
