# Star Standard Library: ui/version_update_dialog
# Description: Software update prompt with release notes and update CTA
# Author: Star Core Team
# Version: 1.0.0

class VersionUpdateDialog
    property name = "version_update_dialog"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VersionUpdateDialog>"
    end
end

function create()
    return VersionUpdateDialog()
end

function describe()
    return "Software update prompt with release notes and update CTA"
end
