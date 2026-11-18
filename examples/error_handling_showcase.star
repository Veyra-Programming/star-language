// ==============================================================================
// Star Error Handling & Runtime Diagnostics Showcase
// Demonstrates try-catch, try-recover, contract assertions, and panic traps.
// ==============================================================================

show "=== 1. Basic Structured Exception Handling (try / catch) ==="

try:
    show "Attempting dangerous division..."
    variable bad_math = 42 / 0
    show "This will not run."
catch error:
    show "Successfully caught exception:"
    show error
end

show ""
show "=== 2. Natural English Recovery (try / recover as err) ==="

try:
    show "Connecting to remote gateway..."
    fail("Connection timed out after 3000ms")
recover as failure:
    show "Gracefully recovered from failure:"
    show failure
end

show ""
show "=== 3. Design by Contract (ensure ... otherwise ...) ==="

function withdraw(balance, amount)
    // Precondition invariant
    ensure amount > 0 otherwise "Withdrawal amount must be positive"
    ensure balance >= amount otherwise "Insufficient funds: balance is less than withdrawal"
    
    variable new_balance = balance - amount
    give back new_balance
end

try:
    variable my_balance = 100
    show "Current balance: 100. Attempting to withdraw 150..."
    variable res = withdraw(my_balance, 150)
    show "Withdrawal completed."
recover as err:
    show "Contract breach trapped:"
    show err
end

show ""
show "=== 4. Explicit Panic Traps (panic / fail) ==="

function process_order(item, quantity)
    whenever quantity <= 0
        panic("Order processing aborted: quantity cannot be zero or negative")
    end
    give back "Order confirmed for " + str(quantity) + " units"
end

try:
    variable order_status = process_order("Compute Node", 0)
    show order_status
catch e:
    show "Order exception caught:"
    show e
end

show ""
show "=== 5. Complete Normal Program Execution Continues Smoothly ==="
show "All runtime exceptions safely handled. Host application alive and healthy!"
