# Star Standard Library: ui/geo_location_input
# Description: Address autocomplete and GPS location capture field
# Author: Star Core Team
# Version: 1.0.0

class GeoLocationInput
    property name = "geo_location_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GeoLocationInput>"
    end
end

function create()
    return GeoLocationInput()
end

function describe()
    return "Address autocomplete and GPS location capture field"
end
