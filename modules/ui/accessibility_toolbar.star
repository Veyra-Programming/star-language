# Star Standard Library: ui/accessibility_toolbar
# Description: Accessibility menu (font resize, high contrast, dyslexia font)
# Author: Star Core Team
# Version: 1.0.0

class AccessibilityToolbar
    property name = "accessibility_toolbar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AccessibilityToolbar>"
    end
end

function create()
    return AccessibilityToolbar()
end

function describe()
    return "Accessibility menu (font resize, high contrast, dyslexia font)"
end
