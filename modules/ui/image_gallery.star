# Star Standard Library: ui/image_gallery
# Description: Multi-thumbnail image gallery with full-screen lightbox
# Author: Star Core Team
# Version: 1.0.0

class ImageGallery
    property name = "image_gallery"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ImageGallery>"
    end
end

function create()
    return ImageGallery()
end

function describe()
    return "Multi-thumbnail image gallery with full-screen lightbox"
end
