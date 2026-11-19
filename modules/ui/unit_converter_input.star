# Star Standard Library: ui/unit_converter_input
# Description: Dual-field imperial to metric live converter input
# Author: Star Core Team
# Version: 1.0.0

class UnitConverterInput
    property name = "unit_converter_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: UnitConverterInput>"
    end
end

function create()
    return UnitConverterInput()
end

function describe()
    return "Dual-field imperial to metric live converter input"
end
