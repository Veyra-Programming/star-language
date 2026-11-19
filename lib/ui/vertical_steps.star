# Star Standard Library: ui/vertical_steps
# Description: Vertical checkout and onboarding progress step tracker
# Author: Star Core Team
# Version: 1.0.0

class VerticalSteps
    property name = "vertical_steps"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VerticalSteps>"
    end
end

function create()
    return VerticalSteps()
end

function describe()
    return "Vertical checkout and onboarding progress step tracker"
end
