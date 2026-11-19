# Star Standard Library: ui/clipboard_copy_button
# Description: Click-to-copy button with checkmark feedback
# Author: Star Core Team
# Version: 1.0.0

class ClipboardCopyButton
    property name = "clipboard_copy_button"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ClipboardCopyButton>"
    end
end

function create()
    return ClipboardCopyButton()
end

function describe()
    return "Click-to-copy button with checkmark feedback"
end
