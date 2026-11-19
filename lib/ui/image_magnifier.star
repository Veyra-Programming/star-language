# Star Standard Library: ui/image_magnifier
# Description: E-commerce product image zoom lens magnifier
# Author: Star Core Team
# Version: 1.0.0

class ImageMagnifier
    property name = "image_magnifier"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ImageMagnifier>"
    end
end

function create()
    return ImageMagnifier()
end

function describe()
    return "E-commerce product image zoom lens magnifier"
end
