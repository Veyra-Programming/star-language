# Star Standard Library: ui/file_drop_zone
# Description: Dashed border drag-and-drop file receiver with MIME filter
# Author: Star Core Team
# Version: 1.0.0

class FileDropZone
    property name = "file_drop_zone"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FileDropZone>"
    end
end

function create()
    return FileDropZone()
end

function describe()
    return "Dashed border drag-and-drop file receiver with MIME filter"
end
