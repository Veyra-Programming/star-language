# Star Standard Library: media/audio_synth
# Description: Waveform synthesis for sine, square, and triangle waves
# Author: Star Core Team
# Version: 1.0.0

class AudioSynth
    property name = "audio_synth"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return AudioSynth()
end

function describe()
    return "Waveform synthesis for sine, square, and triangle waves"
end
