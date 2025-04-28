// This function calculates the factorial
// of a number using recursion.

function factorial(n) {
    if (n === 0) return 1; // base case
    return n * factorial(n - 1); // recursive call
}


// We now test the function
// with a few values

console.log(factorial(0));  // should return 1
console.log(factorial(5));  // should return 120


// End of example
