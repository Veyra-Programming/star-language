# Star Standard Library: ui/segmented_picker
# Description: iOS-style pill segmented control with sliding indicator
# Author: Star Core Team
# Version: 1.0.0

class SegmentedPicker
    property name = "segmented_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SegmentedPicker>"
    end
end

function create()
    return SegmentedPicker()
end

function describe()
    return "iOS-style pill segmented control with sliding indicator"
end
