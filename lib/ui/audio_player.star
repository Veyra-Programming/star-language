# Star Standard Library: ui/audio_player
# Description: Audio playback bar with play/pause, scrub bar, and duration
# Author: Star Core Team
# Version: 1.0.0

class AudioPlayer
    property name = "audio_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AudioPlayer>"
    end
end

function create()
    return AudioPlayer()
end

function describe()
    return "Audio playback bar with play/pause, scrub bar, and duration"
end
