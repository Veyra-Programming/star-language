# Star Standard Library: game/input_manager
# Description: Keyboard and gamepad button state tracker
# Author: Star Core Team
# Version: 1.0.0

class InputManager
    property name = "input_manager"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return InputManager()
end

function describe()
    return "Keyboard and gamepad button state tracker"
end
