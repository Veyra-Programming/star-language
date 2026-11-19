# Star Standard Library: ui/reading_progress_bar
# Description: Top edge reading progress bar tracking page scroll depth
# Author: Star Core Team
# Version: 1.0.0

class ReadingProgressBar
    property name = "reading_progress_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ReadingProgressBar>"
    end
end

function create()
    return ReadingProgressBar()
end

function describe()
    return "Top edge reading progress bar tracking page scroll depth"
end
