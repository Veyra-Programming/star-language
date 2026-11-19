# Star Standard Library: ui/media_object
# Description: Traditional media object layout (left image, right body)
# Author: Star Core Team
# Version: 1.0.0

class MediaObject
    property name = "media_object"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MediaObject>"
    end
end

function create()
    return MediaObject()
end

function describe()
    return "Traditional media object layout (left image, right body)"
end
