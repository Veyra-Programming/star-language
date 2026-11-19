# Star Standard Library: ui/audio_playlist
# Description: Music and podcast playlist manager with queue sorting
# Author: Star Core Team
# Version: 1.0.0

class AudioPlaylist
    property name = "audio_playlist"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AudioPlaylist>"
    end
end

function create()
    return AudioPlaylist()
end

function describe()
    return "Music and podcast playlist manager with queue sorting"
end
