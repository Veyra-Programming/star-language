# Star Standard Library: ui/hero_banner
# Description: Full-width visual hero banner with title, CTA, and background
# Author: Star Core Team
# Version: 1.0.0

class HeroBanner
    property name = "hero_banner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: HeroBanner>"
    end
end

function create()
    return HeroBanner()
end

function describe()
    return "Full-width visual hero banner with title, CTA, and background"
end
