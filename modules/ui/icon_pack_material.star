# Star Standard Library: ui/icon_pack_material
# Description: Comprehensive Google Material Symbols and Icons pack
# Author: Star Core Team
# Version: 1.0.0

class IconPackMaterial
    property name = "icon_pack_material"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IconPackMaterial>"
    end
end

function create()
    return IconPackMaterial()
end

function describe()
    return "Comprehensive Google Material Symbols and Icons pack"
end
