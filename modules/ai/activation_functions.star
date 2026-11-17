# Star Standard Library: ai/activation_functions
# Description: ReLU, Sigmoid, Tanh, and LeakyReLU activation functions
# Author: Star Core Team
# Version: 1.0.0

class ActivationFunctions
    property name = "activation_functions"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ActivationFunctions()
end

function describe()
    return "ReLU, Sigmoid, Tanh, and LeakyReLU activation functions"
end
