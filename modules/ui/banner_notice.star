# Star Standard Library: ui/banner_notice
# Description: Full-width persistent top notification banner
# Author: Star Core Team
# Version: 1.0.0

class BannerNotice
    property name = "banner_notice"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BannerNotice>"
    end
end

function create()
    return BannerNotice()
end

function describe()
    return "Full-width persistent top notification banner"
end
