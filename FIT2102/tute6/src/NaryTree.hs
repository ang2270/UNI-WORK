-- | Implementation of Nary trees.
--
-- The focus of these exercises is to get comfortable with a more
-- complex custom type, and using recursion.
module NaryTree (NaryTree (..), tree, depth, mapTree) where

-- | A NaryTree is a type of tree which has a list of children
--
--
-- See https://tgdwyer.github.io/haskell2/#algebraic-data-types
data NaryTree a = Node a [NaryTree a]
    deriving (Show)

-- Example Trees
tree :: NaryTree Int
tree = Node 2 [Node 3 [Node 41 [], Node 42 [], Node 43 []], Node 5 [Node 6 []]]

-- | Find the depth of a tree (number of levels)
--
-- See https://tgdwyer.github.io/haskell2/#pattern-matching
--
-- >>> depth (Node 1 [])
-- 1
--
-- >>> depth tree
-- 3
depth :: NaryTree a -> Int
depth (Node _ []) = 1
depth (Node _ children) = 1 + maximum (map depth children)

-- | Map a function over a tree.
--
-- >>> mapTree (*1) (Node 1 [])
-- Node 1 []
--
-- >>> mapTree (`mod` 2) tree
-- Node 0 [Node 1 [Node 1 [],Node 0 [],Node 1 []],Node 1 [Node 0 []]]
mapTree :: (a -> b) -> NaryTree a -> NaryTree b
mapTree f (Node v children) = Node (f v) (map (mapTree f) children)  -- Map returns empty list if input is empty ;D
