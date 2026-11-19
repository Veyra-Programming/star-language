# Star Standard Library: ui/video_playlist_carousel
# Description: Video thumbnail playlist with active indicator
# Author: Star Core Team
# Version: 1.0.0

class VideoPlaylistCarousel
    property name = "video_playlist_carousel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VideoPlaylistCarousel>"
    end
end

function create()
    return VideoPlaylistCarousel()
end

function describe()
    return "Video thumbnail playlist with active indicator"
end
