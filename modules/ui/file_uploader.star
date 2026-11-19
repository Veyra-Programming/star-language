# Star Standard Library: ui/file_uploader
# Description: Drag-and-drop multi-file upload zone with progress bars
# Author: Star Core Team
# Version: 1.0.0

class FileUploader
    property name = "file_uploader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FileUploader>"
    end
end

function create()
    return FileUploader()
end

function describe()
    return "Drag-and-drop multi-file upload zone with progress bars"
end
