# Star Standard Library: media/canvas_2d
# Description: 2D drawing command buffer and display list
# Author: Star Core Team
# Version: 1.0.0

class Canvas2d
    property name = "canvas_2d"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Canvas2d()
end

function describe()
    return "2D drawing command buffer and display list"
end
