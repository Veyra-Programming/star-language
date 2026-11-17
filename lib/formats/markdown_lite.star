# Star Standard Library: formats/markdown_lite
# Description: Markdown syntax to HTML converter
# Author: Star Core Team
# Version: 1.0.0

class MarkdownLite
    property name = "markdown_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MarkdownLite()
end

function describe()
    return "Markdown syntax to HTML converter"
end
