# Star Standard Library: ui/video_pip_player
# Description: Picture-in-picture floating mini video player
# Author: Star Core Team
# Version: 1.0.0

class VideoPipPlayer
    property name = "video_pip_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VideoPipPlayer>"
    end
end

function create()
    return VideoPipPlayer()
end

function describe()
    return "Picture-in-picture floating mini video player"
end
