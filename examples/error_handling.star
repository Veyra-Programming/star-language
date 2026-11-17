# Error Handling in Star

show "Attempting dangerous computation..."

try
    variable x = 10
    variable y = 0
    variable z = x / y
    show "Result: " + z
catch err
    show "Handled safely in Star! Error was: " + err
end

show "Execution continues normally after catch block."
