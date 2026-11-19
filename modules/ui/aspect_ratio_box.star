# Star Standard Library: ui/aspect_ratio_box
# Description: Fixed 16:9, 4:3, 1:1 aspect ratio constraint container
# Author: Star Core Team
# Version: 1.0.0

class AspectRatioBox
    property name = "aspect_ratio_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AspectRatioBox>"
    end
end

function create()
    return AspectRatioBox()
end

function describe()
    return "Fixed 16:9, 4:3, 1:1 aspect ratio constraint container"
end
