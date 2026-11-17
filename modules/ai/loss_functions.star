# Star Standard Library: ai/loss_functions
# Description: Mean Squared Error (MSE) and cross-entropy loss
# Author: Star Core Team
# Version: 1.0.0

class LossFunctions
    property name = "loss_functions"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return LossFunctions()
end

function describe()
    return "Mean Squared Error (MSE) and cross-entropy loss"
end
