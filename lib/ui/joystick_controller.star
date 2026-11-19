# Star Standard Library: ui/joystick_controller
# Description: Virtual touch analog joystick for mobile gaming
# Author: Star Core Team
# Version: 1.0.0

class JoystickController
    property name = "joystick_controller"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: JoystickController>"
    end
end

function create()
    return JoystickController()
end

function describe()
    return "Virtual touch analog joystick for mobile gaming"
end
