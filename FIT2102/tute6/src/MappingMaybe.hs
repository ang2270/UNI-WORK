-- | Implementation of Maybe Functions
-- ## Examples
--
-- Defining Maybe values:
--
-- >>> let x = Just 10    -- a Maybe Int containing 10
-- >>> let y = Nothing    -- a Maybe Int with no value
module MappingMaybe (mapMaybe, flatMapMaybe, parseNumber, nonZero, reciprocal, chainFunctions) where

import Text.Read (readMaybe)

-- | Applies a function to the value inside a `Just`, producing a new `Maybe` value.
-- If the input is `Nothing`, it returns `Nothing`.
--
-- >>> mapMaybe (+1) (Just 3)
-- Just 4
--
-- >>> mapMaybe (*2) Nothing
-- Nothing
--
-- >>> mapMaybe reverse (Just "hi")
-- Just "ih"
mapMaybe :: (a -> b) -> Maybe a -> Maybe b
mapMaybe _ Nothing = Nothing
mapMaybe f (Just r) = Just (f r)

-- | Applies a function that returns a `Maybe` to the value inside a `Just`,
-- flattening the result. If the input is `Nothing`, it returns `Nothing`.
--
-- >>> flatMapMaybe nonZero (Just 5)
-- Just 5.0
--
-- >>> flatMapMaybe nonZero (Just 0)
-- Nothing
--
-- >>> flatMapMaybe parseNumber (Just "123")
-- Just 123.0
--
-- >>> flatMapMaybe parseNumber (Just "abc")
-- Nothing
--
-- >>> flatMapMaybe parseNumber Nothing
-- Nothing
flatMapMaybe :: (a -> Maybe b) -> Maybe a -> Maybe b
flatMapMaybe _ Nothing = Nothing
flatMapMaybe f (Just r) = f r

-- | Parse a number from String
-- >>> parseNumber "42.5"
-- Just 42.5
-- >>> parseNumber "foo"
-- Nothing
parseNumber :: String -> Maybe Double
parseNumber = readMaybe 

--   readMaybe :: Read a => String -> Maybe a
--   readMaybe s = case readEither s of
--                 Left _  -> Nothing
--                 Right a -> Just a 

-- | Check non-zero
-- >>> nonZero 0
-- Nothing
-- >>> nonZero 5
-- Just 5.0
nonZero :: Double -> Maybe Double
nonZero 0 = Nothing
nonZero n = Just n

-- | Reciprocal
-- >>> reciprocal 4
-- 0.25
reciprocal :: Double -> Double
reciprocal n = 1 / n

-- Applies a chain of `Maybe`-aware computations to a string:
-- 1. Parses the string to a number
-- 2. Validates that the number is not zero
-- 3. Computes the reciprocal
--
-- >>> chainFunctions "5"
-- Just 0.2
-- >>> chainFunctions "0"
-- Nothing
-- >>> chainFunctions "foo"
-- Nothing
chainFunctions :: String -> Maybe Double
chainFunctions = mapMaybe reciprocal . flatMapMaybe nonZero . parseNumber
