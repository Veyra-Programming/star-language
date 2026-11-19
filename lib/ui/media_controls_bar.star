# Star Standard Library: ui/media_controls_bar
# Description: Universal playback control bar with volume and speed
# Author: Star Core Team
# Version: 1.0.0

class MediaControlsBar
    property name = "media_controls_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MediaControlsBar>"
    end
end

function create()
    return MediaControlsBar()
end

function describe()
    return "Universal playback control bar with volume and speed"
end
