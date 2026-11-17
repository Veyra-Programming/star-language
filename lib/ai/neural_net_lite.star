# Star Standard Library: ai/neural_net_lite
# Description: Feed-forward neural network perceptron layer
# Author: Star Core Team
# Version: 1.0.0

class NeuralNetLite
    property name = "neural_net_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return NeuralNetLite()
end

function describe()
    return "Feed-forward neural network perceptron layer"
end
