# Star Standard Library: mobile/audio_player
# Description: Mobile audio player playback and volume controls
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

end

function create()
    return AudioPlayer()
end

function describe()
    return "Mobile audio player playback and volume controls"
end
