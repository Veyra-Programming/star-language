# Star Standard Library: ui/copy_tooltip
# Description: Click-to-copy button with 'Copied!' temporary tooltip
# Author: Star Core Team
# Version: 1.0.0

class CopyTooltip
    property name = "copy_tooltip"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CopyTooltip>"
    end
end

function create()
    return CopyTooltip()
end

function describe()
    return "Click-to-copy button with 'Copied!' temporary tooltip"
end
