# Star Standard Library: ui/font_picker
# Description: Google Fonts and system typography preview and selection picker
# Author: Star Core Team
# Version: 1.0.0

class FontPicker
    property name = "font_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FontPicker>"
    end
end

function create()
    return FontPicker()
end

function describe()
    return "Google Fonts and system typography preview and selection picker"
end
