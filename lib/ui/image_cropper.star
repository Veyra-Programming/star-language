# Star Standard Library: ui/image_cropper
# Description: Interactive circular and rectangular image crop tool
# Author: Star Core Team
# Version: 1.0.0

class ImageCropper
    property name = "image_cropper"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ImageCropper>"
    end
end

function create()
    return ImageCropper()
end

function describe()
    return "Interactive circular and rectangular image crop tool"
end
