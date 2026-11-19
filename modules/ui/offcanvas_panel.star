# Star Standard Library: ui/offcanvas_panel
# Description: Full-height offcanvas sliding panel from left/right/top/bottom
# Author: Star Core Team
# Version: 1.0.0

class OffcanvasPanel
    property name = "offcanvas_panel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: OffcanvasPanel>"
    end
end

function create()
    return OffcanvasPanel()
end

function describe()
    return "Full-height offcanvas sliding panel from left/right/top/bottom"
end
