# Star Standard Library: ai/linear_regression
# Description: Ordinary least squares slope and intercept calculator
# Author: Star Core Team
# Version: 1.0.0

class LinearRegression
    property name = "linear_regression"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return LinearRegression()
end

function describe()
    return "Ordinary least squares slope and intercept calculator"
end
