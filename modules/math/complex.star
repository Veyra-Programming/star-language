# Star Standard Library: math/complex
# Description: Complex number representation and arithmetic
# Author: Star Core Team
# Version: 1.0.0

class Complex
    property real = 0.0
    property imag = 0.0

    function magnitude()
        return Math.sqrt(self.real * self.real + self.imag * self.imag)
    end

    function conjugate()
        return Complex(real = self.real, imag = 0 - self.imag)
    end

end

function create(r, i)
    return Complex(real = r, imag = i)
end

function add(c1, c2)
    return Complex(real = c1.real + c2.real, imag = c1.imag + c2.imag)
end

function multiply(c1, c2)
    variable r = c1.real * c2.real - c1.imag * c2.imag
    variable i = c1.real * c2.imag + c1.imag * c2.real
    return Complex(real = r, imag = i)
end
