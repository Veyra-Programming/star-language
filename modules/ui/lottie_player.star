# Star Standard Library: ui/lottie_player
# Description: Vector animation player for Lottie JSON animations
# Author: Star Core Team
# Version: 1.0.0

class LottiePlayer
    property name = "lottie_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: LottiePlayer>"
    end
end

function create()
    return LottiePlayer()
end

function describe()
    return "Vector animation player for Lottie JSON animations"
end
