/**
 * IMPORTANT: The README.md file contains important information on getting started.
 * Please read before attempting these exercises.
 *
 * Note that passing tests is just an indication the implementation is not incorrect.
 * Marks are only awarded for correct understanding of the question and demonstration of concepts.
 *
 * Ask a tutor if in doubt!
 */

// Stub value to indicate an implementation
const IMPLEMENT_THIS = undefined;
/*****************************************************************
 * Exercise 1:
 *
 * The const keyword is used for creating an un-reassignable variable.
 * see: https://tgdwyer.github.io/javascript1#declaring-variables
 *
 * Create an un-reassignable variable called firstConst and initialise its value to 1.
 *
 * Then create another un-reassignable variable called secondConst
 *  and initialise its value to firstConst + 1.
 */
const firstConst = 1;
const secondConst = firstConst +1

/*****************************************************************
 * Exercise 2:
 *
 * For this exercise, each function should initialise a local variable with the value 2
 *  and return double its value.
 * see: https://tgdwyer.github.io/javascript1/#functions
 *
 * Create the following functions, each using a different way to declare a function:
 *  - aFunction: using the "function" keyword
 *  - anonymousFunction: using an anonymous function declared with the "function" keyword
 *  - arrowFunction: using an arrow function
 */
function aFunction() {
return 4
}

const anonymousFunction = function(anon) {
    console.log("Wow")
    return 4
}

const arrowFunction = (param1, param2) => {
  return 4
};





/*****************************************************************
 * Exercise 3:
 *
 * Convert a decimal number into its binary representation.
 *
 * How binary numbers work:
 *
 * Each position in a binary number is a power of 2.
 * From right to left:
 *
 * 2^0, 2^1, 2^2, 2^3, 2^4, ...
 *
 * Example:
 * 1101 (binary)
 *
 * = 1 × 2^3
 * + 1 × 2^2
 * + 0 × 2^1
 * + 1 × 2^0
 *
 * = 8 + 4 + 0 + 1
 * = 13 (decimal)
 *
 * Recursive idea:
 * binary(n, acc) = binary(floor(n / 2), (n % 2) + acc)
 *
 * You must use recursion, immutable variables, and pure functions.
 * You must not use loops.
 *****************************************************************/

/**
 * Recursive function that builds a binary string using an accumulator.
 *
 * /Hint/: Each recursive call should divide the number by 2 and prepend
 * the remainder to the accumulator.
 *
 * @param n Decimal number
 * @param acc Accumulator string
 * @returns Binary representation of n
 */
const decimalToBinaryAcc = (n, acc) => {
    // Base case: stop recursion when n reaches 0
    if (n === 0) {
        // When we reach the base case, return the accumulated binary string
        return acc;
    }

    const next = Math.floor(n / 2);
    const newAcc = (n % 2) + acc;
    return decimalToBinaryAcc(next, newAcc);
};

/**
 * Converts a decimal number to binary.
 *
 * /Hint/: Call the accumulator function with an empty string.
 *
 * @param n Decimal number
 * @returns Binary representation of n
 */
const decimalToBinary = n => {
    if (n === 0) {
        return "0";
    }
    return decimalToBinaryAcc(n, "");
};

/*****************************************************************
 * Exercise 4:
 *
 * Practise using array methods.
 * see: https://tgdwyer.github.io/javascript1/#arrays
 */

/**
 * Print each number in the array (one console.log call per number)
 *
 * /Hint/: console.log is used to print
 *
 * @param arr Array to print
 */
const printArray = function(array){
    for (const num of array)
    console.log(num)
}


/**
 * Create a new array with each item incremented by one (1)
 *
 * @param arr Array to increment
 * @returns New array with incremented items
 */
const addOne = function(array){
    for (let i = 0; i < array.length; i++) {
    array[i] = array[i] + 1 }
    return array
}

/**
 * Create a new array with ones removed
 *
 * @param arr Input array
 * @returns Array without ones
 */
const removeOnes = function(array) {
    return array.filter(item => item !== 1);
}
/**
 * Calculate the sum of the items in an array
 *
 * @param arr Input array
 * @returns Sum of items in arr
 */
const sumArray = function(array){
    return array.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
}

const multiplyArray = (n, array) => {
    return array.map(x => x * n);
};

const filterEvenNumbers = array => {
    return array.filter(x => x % 2 === 0);
};

// Do *not* use Math.max
const findMax = array => {
    return array.reduce((max, x) => x > max ? x : max, array[0]);
};

const tripleAndFilterOdds = array => {
    return array
        .map(x => x * 3)
        .filter(x => x % 2 !== 0);
};

const countOddNumbers = array => {
    return array.filter(x => x % 2 !== 0).length;
};

/*****************************************************************
 * Exercise 6:
 *
 * Solve the Project Euler Problem 1 by implementing the following functions.
 *
 * Use only pure array methods.
 *
 * Project Euler Problem 1 is the following:
 *
 * "If we list all the natural numbers below 10 that are multiples of 3 or 5,
 *  we get 3, 5, 6 and 9. The sum of these multiples is 23.
 *  Find the sum of all the multiples of 3 or 5 below 1000."
 */

/**-
 * Create a range of values
 *
 * @param n Target value
 * @returns Array of integers in the range [0, n)
 */
const range = function(n) {
    return Array.from({ length: n }, (_, i) => i);
};

/**
 * @returns Answer to project euler problem 1
 */
const projectEulerProblem1 = () => {
    const array = range(1000)
    return array
    .filter(x => x % 3 === 0 || x % 5 === 0)
    .reduce((total, x) => total + x, 0)
};

/*****************************************************************
 * Exercise 7:
 * This exercise starts to explore functional programming concepts.
 * We will go through this in detail in the Workshop.
 *
 * The Cons list is a simple immutable data structure composing
 *  only of functions, using closures to capture data.
 * see also: https://tgdwyer.github.io/functionaljavascript/#computation-with-pure-functions
 *
 * This is essentially equivalent to linked lists.
 *
 * Implement the following functions to define a Cons list.
 */

/**
 * Cons "constructs" a list node, if no second argument is specified it is the last node in the list
 *
 * @param head Head of cons list, the value to be stored
 * @param rest Tail of cons list, reference to the rest of the cons list
 * @returns Cons list, function in closure
 */
function cons(head, rest = null) {
    return selector => selector(head, rest);
}

/**
 * Head selector
 *
 * @param list Non-empty cons list, remember this is a function!
 * @returns First element in cons list
 */
function head(list) {
    if (!list) throw new TypeError("list is null");

    return list((h, _) => h);
}

/**
 * Rest selector
 *
 * @param list Non-empty cons list, remember this is a function!
 * @returns Rest of the cons list
 */
function rest(list) {
    if (!list) throw new TypeError("list is null");

    return list((_, r) => r);
}

/*****************************************************************
 * Exercise 8
 * This exercise starts to explore functional programming concepts.
 * We will go through this in detail in the Workshop.
 * see https://tgdwyer.github.io/functionaljavascript#computation-with-pure-functions
 *
 * Higher order functions are applicable on any data type we can think of.
 * This, of course, also applies to the Cons list.
 *
 * Implement the following higher order functions for Cons lists.
 */

/**
 * Use this as an example for other functions!
 *
 * @param f Function to use for each element
 * @param list Cons list
 */
function forEach(f, list) {
    if (list) {
        f(head(list));
        forEach(f, rest(list));
    }
}

/**
 * Map for cons list
 *
 * @param f Function to apply
 * @param list Cons list to map
 * @returns New cons list with f applied to elements
 */
function map(f, list) {
    if (!list) return null;

    return cons(f(head(list)), map(f, rest(list)));
}

/**
 * Reduce for cons list
 *
 * @param {(acc, val) => any} f Reducing function, this combines the accumulator with the current value. Note that the accumulator value is the first parameter, and the current value is the second parameter.
 * @param acc Accumulated value, initial value
 * @param list Cons list to reduce
 * @returns The accumulated value after applying f to each element in list, left to right
 */
function reduce(f, acc, list) {
    if (!list) return acc;
    return reduce(f, f(acc, head(list)), rest(list));
}

/**
 * Filter for cons list
 *
 * @param f Function to accept or reject values
 * @param list Cons list to filter
 * @returns New cons list with only accepted values
 */
function filter(f, list) {
    if (!list) return null;

    // Skip value
    if (!f(head(list))) return filter(f, rest(list));

    return cons(head(list), filter(f, rest(list)));
}
