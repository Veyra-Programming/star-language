# Star Standard Library: ui/barcode_display
# Description: UPC, EAN, and Code128 barcode generator view
# Author: Star Core Team
# Version: 1.0.0

class BarcodeDisplay
    property name = "barcode_display"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BarcodeDisplay>"
    end
end

function create()
    return BarcodeDisplay()
end

function describe()
    return "UPC, EAN, and Code128 barcode generator view"
end
