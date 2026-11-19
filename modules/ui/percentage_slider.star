# Star Standard Library: ui/percentage_slider
# Description: Continuous 0-100% percentage slider with colored track
# Author: Star Core Team
# Version: 1.0.0

class PercentageSlider
    property name = "percentage_slider"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PercentageSlider>"
    end
end

function create()
    return PercentageSlider()
end

function describe()
    return "Continuous 0-100% percentage slider with colored track"
end
