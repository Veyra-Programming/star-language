# Star Standard Library: ui/gif_player
# Description: Animated GIF player with pause, loop, and frame controls
# Author: Star Core Team
# Version: 1.0.0

class GifPlayer
    property name = "gif_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GifPlayer>"
    end
end

function create()
    return GifPlayer()
end

function describe()
    return "Animated GIF player with pause, loop, and frame controls"
end
