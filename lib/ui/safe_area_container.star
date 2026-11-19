# Star Standard Library: ui/safe_area_container
# Description: Mobile notch and home-bar safe area padding container
# Author: Star Core Team
# Version: 1.0.0

class SafeAreaContainer
    property name = "safe_area_container"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SafeAreaContainer>"
    end
end

function create()
    return SafeAreaContainer()
end

function describe()
    return "Mobile notch and home-bar safe area padding container"
end
