# Star Standard Library: media/bitmap_font
# Description: 5x7 pixel bitmap ASCII font glyph renderer
# Author: Star Core Team
# Version: 1.0.0

class BitmapFont
    property name = "bitmap_font"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BitmapFont()
end

function describe()
    return "5x7 pixel bitmap ASCII font glyph renderer"
end
