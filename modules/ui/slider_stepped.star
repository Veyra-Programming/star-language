# Star Standard Library: ui/slider_stepped
# Description: Discrete stepped numeric slider with tick marks
# Author: Star Core Team
# Version: 1.0.0

class SliderStepped
    property name = "slider_stepped"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SliderStepped>"
    end
end

function create()
    return SliderStepped()
end

function describe()
    return "Discrete stepped numeric slider with tick marks"
end
