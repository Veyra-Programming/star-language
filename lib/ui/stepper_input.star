# Star Standard Library: ui/stepper_input
# Description: Incremental numeric +/- stepper with min/max bounds
# Author: Star Core Team
# Version: 1.0.0

class StepperInput
    property name = "stepper_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StepperInput>"
    end
end

function create()
    return StepperInput()
end

function describe()
    return "Incremental numeric +/- stepper with min/max bounds"
end
