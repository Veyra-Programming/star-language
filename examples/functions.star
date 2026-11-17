# Functions and Closures in Star

function greet(name, title)
    return "Greetings, " + title + " " + name + "!"
end

show greet("Alex", "Commander")

# Closures
function createMultiplier(factor)
    function multiply(x)
        return x * factor
    end
    return multiply
end

variable double = createMultiplier(2)
variable triple = createMultiplier(3)

show "Double 15 = " + double(15)
show "Triple 15 = " + triple(15)
