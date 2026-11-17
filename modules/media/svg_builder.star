# Star Standard Library: media/svg_builder
# Description: SVG vector graphic path and shape builder
# Author: Star Core Team
# Version: 1.0.0

class SvgBuilder
    property name = "svg_builder"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SvgBuilder()
end

function describe()
    return "SVG vector graphic path and shape builder"
end
