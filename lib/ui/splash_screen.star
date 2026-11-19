# Star Standard Library: ui/splash_screen
# Description: Initial application loading splash view with logo fade
# Author: Star Core Team
# Version: 1.0.0

class SplashScreen
    property name = "splash_screen"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SplashScreen>"
    end
end

function create()
    return SplashScreen()
end

function describe()
    return "Initial application loading splash view with logo fade"
end
