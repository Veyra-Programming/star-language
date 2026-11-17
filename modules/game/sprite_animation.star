# Star Standard Library: game/sprite_animation
# Description: Sprite sheet frame counter and animation sequence
# Author: Star Core Team
# Version: 1.0.0

class SpriteAnimation
    property name = "sprite_animation"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SpriteAnimation()
end

function describe()
    return "Sprite sheet frame counter and animation sequence"
end
