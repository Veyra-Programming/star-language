# Star Standard Library: media/wav_writer
# Description: WAV PCM audio file header encoder
# Author: Star Core Team
# Version: 1.0.0

class WavWriter
    property name = "wav_writer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return WavWriter()
end

function describe()
    return "WAV PCM audio file header encoder"
end
