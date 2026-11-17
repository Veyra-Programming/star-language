# Star Standard Library: media/waveform
# Description: Audio sample peak and RMS amplitude calculator
# Author: Star Core Team
# Version: 1.0.0

class Waveform
    property name = "waveform"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Waveform()
end

function describe()
    return "Audio sample peak and RMS amplitude calculator"
end
