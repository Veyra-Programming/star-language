# Star Standard Library: ui/file_browser_grid
# Description: Grid and list file manager with file type icons and sizes
# Author: Star Core Team
# Version: 1.0.0

class FileBrowserGrid
    property name = "file_browser_grid"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FileBrowserGrid>"
    end
end

function create()
    return FileBrowserGrid()
end

function describe()
    return "Grid and list file manager with file type icons and sizes"
end
