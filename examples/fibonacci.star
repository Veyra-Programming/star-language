# Fibonacci calculation demonstrating recursion and loops in Star

function fibRecursive(n)
    if n <= 1
        return n
    end
    return fibRecursive(n - 1) + fibRecursive(n - 2)
end

show "Recursive Fibonacci:"
show "fib(0) = " + fibRecursive(0)
show "fib(1) = " + fibRecursive(1)
show "fib(6) = " + fibRecursive(6)
show "fib(10) = " + fibRecursive(10)

show ""
show "Iterative Sequence:"
variable a = 0
variable b = 1
variable count = 0

while count < 8
    show a
    variable temp = a + b
    a = b
    b = temp
    count = count + 1
end