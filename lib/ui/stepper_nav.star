# Star Standard Library: ui/stepper_nav
# Description: Step-by-step wizard navigation with completed badges
# Author: Star Core Team
# Version: 1.0.0

class StepperNav
    property name = "stepper_nav"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StepperNav>"
    end
end

function create()
    return StepperNav()
end

function describe()
    return "Step-by-step wizard navigation with completed badges"
end
