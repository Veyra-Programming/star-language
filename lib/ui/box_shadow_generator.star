# Star Standard Library: ui/box_shadow_generator
# Description: Visual drop-shadow and elevation tuner with preview
# Author: Star Core Team
# Version: 1.0.0

class BoxShadowGenerator
    property name = "box_shadow_generator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BoxShadowGenerator>"
    end
end

function create()
    return BoxShadowGenerator()
end

function describe()
    return "Visual drop-shadow and elevation tuner with preview"
end
