# Star Standard Library: ui/icon_pack_lucide
# Description: Modern, beautiful Lucide vector icon pack
# Author: Star Core Team
# Version: 1.0.0

class IconPackLucide
    property name = "icon_pack_lucide"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IconPackLucide>"
    end
end

function create()
    return IconPackLucide()
end

function describe()
    return "Modern, beautiful Lucide vector icon pack"
end
