# Star Standard Library: ui/sound_effect_button
# Description: Interactive button with integrated WebAudio click sound
# Author: Star Core Team
# Version: 1.0.0

class SoundEffectButton
    property name = "sound_effect_button"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SoundEffectButton>"
    end
end

function create()
    return SoundEffectButton()
end

function describe()
    return "Interactive button with integrated WebAudio click sound"
end
