# Star Standard Library: math/fraction
# Description: Rational number fraction representations and exact arithmetic
# Author: Star Core Team
# Version: 1.0.0

class Fraction
    property num = 0
    property den = 1

    function to_decimal()
        return self.num * 1.0 / self.den
    end

    function to_string()
        return "" + self.num + "/" + self.den
    end

end

function create(n, d)
    return Fraction(num = n, den = d)
end

function add(f1, f2)
    variable n = f1.num * f2.den + f2.num * f1.den
    variable d = f1.den * f2.den
    return Fraction(num = n, den = d)
end

function multiply(f1, f2)
    return Fraction(num = f1.num * f2.num, den = f1.den * f2.den)
end
