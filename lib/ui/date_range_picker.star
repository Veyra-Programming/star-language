# Star Standard Library: ui/date_range_picker
# Description: Dual calendar date span and range selector
# Author: Star Core Team
# Version: 1.0.0

class DateRangePicker
    property name = "date_range_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DateRangePicker>"
    end
end

function create()
    return DateRangePicker()
end

function describe()
    return "Dual calendar date span and range selector"
end
