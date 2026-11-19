# Star Standard Library: ui/carousel_slider
# Description: Touch swipeable media carousel with autoplay and arrows
# Author: Star Core Team
# Version: 1.0.0

class CarouselSlider
    property name = "carousel_slider"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CarouselSlider>"
    end
end

function create()
    return CarouselSlider()
end

function describe()
    return "Touch swipeable media carousel with autoplay and arrows"
end
