# Star Standard Library: ui/icon_font_viewer
# Description: Interactive searchable icon font glyph inspector
# Author: Star Core Team
# Version: 1.0.0

class IconFontViewer
    property name = "icon_font_viewer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IconFontViewer>"
    end
end

function create()
    return IconFontViewer()
end

function describe()
    return "Interactive searchable icon font glyph inspector"
end
