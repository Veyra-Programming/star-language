# Star Standard Library: ui/media_list_item
# Description: Media item with thumbnail, title, description, and metadata
# Author: Star Core Team
# Version: 1.0.0

class MediaListItem
    property name = "media_list_item"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MediaListItem>"
    end
end

function create()
    return MediaListItem()
end

function describe()
    return "Media item with thumbnail, title, description, and metadata"
end
