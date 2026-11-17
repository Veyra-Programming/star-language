# Star Standard Library: game/entity_component
# Description: Entity-Component-System (ECS) architecture
# Author: Star Core Team
# Version: 1.0.0

class EntityComponent
    property name = "entity_component"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return EntityComponent()
end

function describe()
    return "Entity-Component-System (ECS) architecture"
end
