# Star Standard Library: ui/step_progress
# Description: Multi-phase linear step progress tracker with checkmarks
# Author: Star Core Team
# Version: 1.0.0

class StepProgress
    property name = "step_progress"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StepProgress>"
    end
end

function create()
    return StepProgress()
end

function describe()
    return "Multi-phase linear step progress tracker with checkmarks"
end
