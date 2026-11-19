# Star Standard Library: ui/time_duration_picker
# Description: Hours, minutes, seconds duration timer picker
# Author: Star Core Team
# Version: 1.0.0

class TimeDurationPicker
    property name = "time_duration_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TimeDurationPicker>"
    end
end

function create()
    return TimeDurationPicker()
end

function describe()
    return "Hours, minutes, seconds duration timer picker"
end
