# Star Standard Library: ui/time_picker
# Description: Clock face and 24h/12h time selector widget
# Author: Star Core Team
# Version: 1.0.0

class TimePicker
    property name = "time_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TimePicker>"
    end
end

function create()
    return TimePicker()
end

function describe()
    return "Clock face and 24h/12h time selector widget"
end
