# Star Standard Library: math/bigint
# Description: Arbitrary-precision integer emulation using digit string arithmetic
# Author: Star Core Team
# Version: 1.0.0

class BigInt
    property digits = "0"
    property negative = false

    function to_string()
        if self.negative
        return "-" + self.digits
        end
        return self.digits
    end

    function is_zero()
        return self.digits == "0"
    end

end

function from_string(s)
    return BigInt(digits = s, negative = false)
end

function compare_len(a, b)
    return len(a.digits) - len(b.digits)
end
