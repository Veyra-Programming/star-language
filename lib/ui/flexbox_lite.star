# Star Standard Library: ui/flexbox_lite
# Description: Flex layout direction, alignment, and justification
# Author: Star Core Team
# Version: 1.0.0

class FlexboxLite
    property name = "flexbox_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FlexboxLite()
end

function describe()
    return "Flex layout direction, alignment, and justification"
end
