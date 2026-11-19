# Star Standard Library: ui/image_comparison_slider
# Description: Before-and-after image comparison slider
# Author: Star Core Team
# Version: 1.0.0

class ImageComparisonSlider
    property name = "image_comparison_slider"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ImageComparisonSlider>"
    end
end

function create()
    return ImageComparisonSlider()
end

function describe()
    return "Before-and-after image comparison slider"
end
