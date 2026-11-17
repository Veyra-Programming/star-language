# Star Standard Library: media/pixel_buffer
# Description: 2D pixel grid manipulation and color filling
# Author: Star Core Team
# Version: 1.0.0

class PixelBuffer
    property name = "pixel_buffer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return PixelBuffer()
end

function describe()
    return "2D pixel grid manipulation and color filling"
end
