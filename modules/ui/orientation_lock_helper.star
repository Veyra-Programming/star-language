# Star Standard Library: ui/orientation_lock_helper
# Description: Mobile landscape/portrait orientation prompt overlay
# Author: Star Core Team
# Version: 1.0.0

class OrientationLockHelper
    property name = "orientation_lock_helper"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: OrientationLockHelper>"
    end
end

function create()
    return OrientationLockHelper()
end

function describe()
    return "Mobile landscape/portrait orientation prompt overlay"
end
