# Module and Standard Library Demo in Star 0.2

use Math
use String
use "examples/helpers.star"

show "Math constants & functions:"
show "PI = " + Math.PI
show "sqrt(144) = " + Math.sqrt(144)
show "pow(2, 8) = " + Math.pow(2, 8)
show "max(45, 99) = " + Math.max(45, 99)

show ""
show "String utilities:"
variable raw = "   star language   "
show "Trimmed: '" + String.trim(raw) + "'"
show "Uppercase: " + String.uppercase(raw)

show ""
show "Local module import:"
variable price = 120.0
variable tax = helpers.calculateTax(price, 0.15)
show "Subtotal: " + helpers.formatCurrency(price)
show "Tax (15%): " + helpers.formatCurrency(tax)
show "Total: " + helpers.formatCurrency(price + tax)
