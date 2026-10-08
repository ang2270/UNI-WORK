-- | Implementation of integer valued binary trees.
--
-- The focus of these exercises is to get comfortable with a more
-- complex custom type, and using recursion.
module BinTree (BinTree (..), tree, one, depth, mapTree) where

-- | A BinTree is a type of tree which has two children: a left and a right.
--
-- The children can be either
-- - a Leaf with no value, or
-- - another BinTree
--
-- See https://tgdwyer.github.io/haskell2/#algebraic-data-types
data BinTree a = Leaf | Node a (BinTree a) (BinTree a)
    deriving (Show)

-- Example Trees
tree :: BinTree Int
tree = Node 16 (Node 23 Leaf (Node 73 Leaf Leaf)) (Node 42 Leaf Leaf)

one :: BinTree Int
one = Node 1 Leaf Leaf

-- | Find the depth of a tree (number of levels)
--
-- See https://tgdwyer.github.io/haskell2/#pattern-matching
--
-- >>> depth Leaf
-- 0
--
-- >>> depth (Node 1 Leaf Leaf)
-- 1
--
-- >>> depth tree
-- 3
depth :: BinTree a -> Int
depth Leaf = 0
depth (Node val left right) = 1 + max (depth left) (depth right)

-- | Map a function over a tree.
--
-- >>> mapTree (+1) Leaf
-- Leaf
--
-- >>> mapTree (*1) one
-- Node 1 Leaf Leaf
--
-- >>> mapTree (`mod` 2) tree
-- Node 0 (Node 1 Leaf (Node 1 Leaf Leaf)) (Node 0 Leaf Leaf)
mapTree :: (a -> b) -> BinTree a -> BinTree b
mapTree f Leaf = Leaf 
mapTree f (Node val left right) = Node (f val) (mapTree f left) (mapTree f right)

