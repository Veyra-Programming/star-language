# Star Standard Library: ui/subtitles_overlay
# Description: Synchronized closed captions and video subtitles overlay
# Author: Star Core Team
# Version: 1.0.0

class SubtitlesOverlay
    property name = "subtitles_overlay"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SubtitlesOverlay>"
    end
end

function create()
    return SubtitlesOverlay()
end

function describe()
    return "Synchronized closed captions and video subtitles overlay"
end
