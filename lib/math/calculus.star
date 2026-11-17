# Star Standard Library: math/calculus
# Description: Numerical differentiation and integration approximations
# Author: Star Core Team
# Version: 1.0.0

class Differentiator
    property epsilon = 0.0001

    function get_epsilon()
        return self.epsilon
    end

end

function derivative_approx(f, x, h)
    return (f(x + h) - f(x - h)) / (2.0 * h)
end

function trapezoid_rule(f, a, b, n)
    variable h = (b - a) / n
    variable s = 0.5 * (f(a) + f(b))
    variable i = 1
    while i < n
    s = s + f(a + i * h)
    i = i + 1
    end
    return s * h
end
