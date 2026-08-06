from __future__ import annotations
from dataclasses import dataclass

import personality
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality
from data_structures.linked_stack import LinkedStack


# Extra function to improve readability
def choice(personality: WalkerPersonality, trail):
    top = trail.store.top
    bot = trail.store.bottom
    return personality.select_branch(top, bot)

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.following.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
        return TrailSeries(mountain=None, following= self.following)

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        new_following = TrailSeries(mountain=self.mountain,following=self.following)
        return TrailSeries(mountain=mountain, following=Trail(store=new_following))

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        empty_trail = Trail(None)
        new_following = TrailSeries(mountain=self.mountain,following=self.following)
        return TrailSplit(top=empty_trail, bottom=empty_trail, following=Trail(store=new_following))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        new_following = TrailSeries(mountain=mountain,following=self.following)
        return TrailSeries(mountain=self.mountain, following=Trail(store=new_following))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        empty_trail = Trail()  # Create an empty Trail
        new_following = TrailSplit(top=empty_trail, bottom=empty_trail, following=self.following)
        return TrailSeries(mountain=self.mountain, following=Trail(store=new_following))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        new_trail = TrailSeries(mountain=mountain, following=Trail(store=self.store))
        return Trail(store=new_trail)

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        empty_trail = Trail()
        new_trail = TrailSplit(top=empty_trail, bottom=empty_trail, following=Trail(store=self.store))
        return Trail(store=new_trail)

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        """ TIME COMPLEXTIY: Worst Case: O(n) where n is the number of elements in the trail. Best Case: O(1) if nothing is stored in the trail"""
        my_stack = LinkedStack()
        stopped = False

        stack_current = self
        my_stack.push(stack_current)

        while stack_current.store is not None and stopped == False:
            if isinstance(stack_current.store, TrailSplit):
                result = choice(personality, stack_current)
                if result.name == "TOP":
                    stack_current = stack_current.store.top
                    my_stack.push(stack_current)
                elif result.name == "BOTTOM":
                    stack_current = stack_current.store.bottom
                    my_stack.push(stack_current)
                elif result.name == "STOP":
                    stopped = True

            else:
                stack_current = stack_current.store.following
                if stack_current.store is not None:
                    my_stack.push(stack_current)

        while not my_stack.is_empty():
            if stopped == True:
                popped = my_stack.pop()
                if isinstance(popped.store, TrailSeries):
                    if popped.store.mountain:
                        personality.add_mountain(popped.store.mountain)
                else:
                    continue
            else:
                popped = my_stack.pop()
                if isinstance(popped.store, TrailSeries):
                    if popped.store.mountain:
                        personality.add_mountain(popped.store.mountain)
                else:
                    if popped.store == None:
                        continue
                    else:
                        check = popped.store.following
                        if isinstance(check.store, TrailSeries):
                            my_stack.push(check)




    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        """TIME COMPLEXITY: Best case O(1) - no mountains/trail
           Worst case O(n) where n^2 is the number of elements in the trail"""
        mountains = []
        current_trail = self

        while current_trail is not None:
            if isinstance(current_trail.store, TrailSeries):
                if current_trail.store.mountain is not None:
                    mountains.append(current_trail.store.mountain)
                current_trail = current_trail.store.following
            elif isinstance(current_trail.store, TrailSplit):
                possbility_stack = LinkedStack()
                possbility_stack.push(current_trail.store.top)
                possbility_stack.push(current_trail.store.bottom)
                # Traverse both top and bottom branches
                current_trail = current_trail.store.following
            else:
                # No more trail to follow
                break

        while not possbility_stack.is_empty():
            current_trail = possbility_stack.pop()
            while current_trail is not None:
                if isinstance(current_trail.store, TrailSeries):
                    if current_trail.store.mountain is not None:
                        mountains.append(current_trail.store.mountain)
                    current_trail = current_trail.store.following
                elif isinstance(current_trail.store, TrailSplit):
                    possbility_stack.push(current_trail.store.top)
                    possbility_stack.push(current_trail.store.bottom)
                    current_trail = current_trail.store.following
                else:
                    # No more trail to follow
                 break
        return mountains

    def difficulty_maximum_paths(self, max_difficulty: int) -> List[List[Mountain]]:
        def dfs(node, current_path, result):
            if isinstance(node.store, TrailSeries):
                if node.store.mountain:
                    if node.store.mountain.difficulty_level < max_difficulty:
                        current_path.append(node.store.mountain)
                        dfs(node.store.following, current_path, result)
                        current_path.pop()
                    else:
                        return
            elif isinstance(node.store, TrailSplit):
                top_path = current_path.copy()
                bottom_path = current_path.copy()

                # Traverse the top branch if it exists and is not None
                if node.store.top:
                    dfs(node.store.top, top_path, result)

                # Traverse the bottom branch if it exists and is not None
                if node.store.bottom:
                    dfs(node.store.bottom, bottom_path, result)

            # Check if any mountain in the current path exceeds the max difficulty
            if not isinstance(node.store, TrailSeries):
                if any(m.difficulty_level > max_difficulty for m in current_path):
                    return

            # Add the current path to the result
            result.append(current_path[:])

        result = []
        current_path = []
        dfs(self, current_path, result)
        return result

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
