# Star Standard Library: mobile/geolocation
# Description: GPS coordinates and Haversine distance calculator
# Author: Star Core Team
# Version: 1.0.0

class Geolocation
    property name = "geolocation"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Geolocation()
end

function describe()
    return "GPS coordinates and Haversine distance calculator"
end
