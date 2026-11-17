# Star Standard Library: media/midi_lite
# Description: MIDI note-on, note-off, and controller events
# Author: Star Core Team
# Version: 1.0.0

class MidiLite
    property name = "midi_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MidiLite()
end

function describe()
    return "MIDI note-on, note-off, and controller events"
end
