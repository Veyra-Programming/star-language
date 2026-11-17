# Star Standard Library: ui/box_model
# Description: CSS box model margins, paddings, and borders
# Author: Star Core Team
# Version: 1.0.0

class BoxModel
    property name = "box_model"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BoxModel()
end

function describe()
    return "CSS box model margins, paddings, and borders"
end
