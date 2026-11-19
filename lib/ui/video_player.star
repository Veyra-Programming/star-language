# Star Standard Library: ui/video_player
# Description: Responsive HTML5 and native video player with custom controls
# Author: Star Core Team
# Version: 1.0.0

class VideoPlayer
    property name = "video_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VideoPlayer>"
    end
end

function create()
    return VideoPlayer()
end

function describe()
    return "Responsive HTML5 and native video player with custom controls"
end
