# Star Standard Library: ui/pdf_viewer
# Description: Embedded PDF document viewer with page navigation and zoom
# Author: Star Core Team
# Version: 1.0.0

class PdfViewer
    property name = "pdf_viewer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PdfViewer>"
    end
end

function create()
    return PdfViewer()
end

function describe()
    return "Embedded PDF document viewer with page navigation and zoom"
end
