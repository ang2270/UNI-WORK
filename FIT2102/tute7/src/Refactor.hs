{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore #-}

-- | Refactor the following functions to
-- - use list methods instead of recursion
-- - use guards/pattern matching/case-of expressions instead of if expressions
module Refactor (doubleAll, flipBools, sumPositives, grade, classify, avgPositives) where

-- |
-- Doubles every number in a list.
--
-- >>> doubleAll []
-- []
--
-- >>> doubleAll [1,2,3]
-- [2,4,6]
--
-- >>> doubleAll [0,-3]
-- [0,-6]
doubleAll :: [Int] -> [Int]
doubleAll [] = []
doubleAll x = map (*2) x

-- |
-- Negates every Bool in a list.
--
-- >>> flipBools []
-- []
--
-- >>> flipBools [True, False, True]
-- [False,True,False]
--
-- >>> flipBools (replicate 4 True)
-- [False,False,False,False]
flipBools :: [Bool] -> [Bool]
flipBools [] = []
flipBools x = map not x

-- |
-- Sums only the positive integers in a list.
--
-- >>> sumPositives []
-- 0
--
-- >>> sumPositives [1,-2,3,0]
-- 4
--
-- >>> sumPositives [-5,-1]
-- 0
--
-- >>> sumPositives [10, -1, 2, -3, 4]
-- 16
sumPositives :: [Int] -> Int
sumPositives [] = 0
sumPositives x = sum (filter (\(a) -> a > 0) x) 
-- Lambda!

-- |
-- Returns a letter grade for a score.
--
-- >>> map grade [95, 84, 73, 65, 12]
-- ["HD","HD","D","C","N"]
grade :: Int -> String
grade n 
    | n >= 80 = "HD"
    | n >= 70 = "D"
    | n >= 60 = "C"
    | n >= 50 = "P"
    | otherwise = "N"


-- |
-- Classifies an integer as "zero", "positive", or "negative".
-- This version uses a clumsy @case True of@ with guards, which is
-- considered an anti-pattern (good refactoring target).
--
-- >>> classify 0
-- "zero"
--
-- >>> classify 5
-- "positive"
--
-- >>> classify (-2)
-- "negative"
classify :: Int -> String
classify n
    | n == 0 = "zero"
    | n > 0 = "positive"
    | otherwise = "negative"

-- |
-- Computes the average of all positive numbers in a list of Doubles.
-- If no positive numbers, return Nothing
--
-- >>> avgPositives []
-- Nothing
--
-- >>> avgPositives [-3.5, -2.0, 0.0]
-- Nothing
--
-- >>> avgPositives [1.0, -2.0, 3.0, 4.0]
-- Just 2.6666666666666665
--
-- >>> avgPositives [10.0, 20.0]
-- Just 15.0
avgPositives :: [Double] -> Maybe Double
avgPositives [] = Nothing
avgPositives x =
    case filter (\(a) -> a>0) x of  
        [] -> Nothing
        a -> Just (sum a / fromIntegral (length a))


--  sum (filter (\(a) -> a > 0) x) 