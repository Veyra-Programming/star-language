# Star Standard Library: ai/logistic_regression
# Description: Sigmoid probability classifier
# Author: Star Core Team
# Version: 1.0.0

class LogisticRegression
    property name = "logistic_regression"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return LogisticRegression()
end

function describe()
    return "Sigmoid probability classifier"
end
