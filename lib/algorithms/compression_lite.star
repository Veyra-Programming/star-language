# Star Standard Library: algorithms/compression_lite
# Description: Run-length encoding (RLE) and frequency counting
# Author: Star Core Team
# Version: 1.0.0

class CompressionLite
    property name = "compression_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CompressionLite()
end

function describe()
    return "Run-length encoding (RLE) and frequency counting"
end
