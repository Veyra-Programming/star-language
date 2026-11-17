# Star Standard Library: mobile/torch
# Description: Flashlight hardware controller simulation
# Author: Star Core Team
# Version: 1.0.0

class Torch
    property name = "torch"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Torch()
end

function describe()
    return "Flashlight hardware controller simulation"
end
