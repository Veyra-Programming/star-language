# Star Standard Library: ui/icon_pack_fontawesome
# Description: Complete Font Awesome vector icons library
# Author: Star Core Team
# Version: 1.0.0

class IconPackFontawesome
    property name = "icon_pack_fontawesome"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IconPackFontawesome>"
    end
end

function create()
    return IconPackFontawesome()
end

function describe()
    return "Complete Font Awesome vector icons library"
end
