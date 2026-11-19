# Star Standard Library: ui/lazy_image_loader
# Description: Intersection-observer powered lazy image loader
# Author: Star Core Team
# Version: 1.0.0

class LazyImageLoader
    property name = "lazy_image_loader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: LazyImageLoader>"
    end
end

function create()
    return LazyImageLoader()
end

function describe()
    return "Intersection-observer powered lazy image loader"
end
