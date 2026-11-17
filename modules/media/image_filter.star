# Star Standard Library: media/image_filter
# Description: Image filters (grayscale, brightness, invert)
# Author: Star Core Team
# Version: 1.0.0

class ImageFilter
    property name = "image_filter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ImageFilter()
end

function describe()
    return "Image filters (grayscale, brightness, invert)"
end
