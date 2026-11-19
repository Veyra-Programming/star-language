# Star Standard Library: ui/word_cloud
# Description: Frequency-weighted semantic word cloud layout
# Author: Star Core Team
# Version: 1.0.0

class WordCloud
    property name = "word_cloud"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: WordCloud>"
    end
end

function create()
    return WordCloud()
end

function describe()
    return "Frequency-weighted semantic word cloud layout"
end
