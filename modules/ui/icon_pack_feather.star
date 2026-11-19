# Star Standard Library: ui/icon_pack_feather
# Description: Simply beautiful open-source Feather icon pack
# Author: Star Core Team
# Version: 1.0.0

class IconPackFeather
    property name = "icon_pack_feather"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IconPackFeather>"
    end
end

function create()
    return IconPackFeather()
end

function describe()
    return "Simply beautiful open-source Feather icon pack"
end
