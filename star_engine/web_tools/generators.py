"""
Star Web Tools — Artisan-style Scaffolding & Code Generators
Authoritative Reference: STAR_WEB_TOOLS_SPEC.md
"""

import os
import time


class WebGenerators:
    """Scaffolds modern web components, pages, APIs, and models."""

    @classmethod
    def make_page(cls, name: str, directory: str = "views") -> str:
        os.makedirs(directory, exist_ok=True)
        filename = f"{name}.star.html"
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            raise FileExistsError(f"Page file already exists: '{path}'")

        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title | escape }}}}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; margin: 40px; line-height: 1.6; background: #0f172a; color: #f8fafc; }}
        .card {{ background: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; max-width: 600px; }}
        h1 {{ color: #38bdf8; margin-top: 0; }}
        .badge {{ background: #0284c7; padding: 4px 10px; border-radius: 999px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">STAR WEB TEMPLATE</span>
        <h1>{{{{ heading }}}}</h1>
        <p>{{{{ message }}}}</p>
        
        {{% whenever user %}}
            <p>Welcome back, <strong>{{{{ user.name }}}}</strong>!</p>
        {{% otherwise %}}
            <p>Please log in to continue.</p>
        {{% end %}}

        <ul>
            {{% for each item in items %}}
                <li>Item: {{{{ item }}}}</li>
            {{% end %}}
        </ul>
    </div>
</body>
</html>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    @classmethod
    def make_api(cls, name: str, directory: str = "routes") -> str:
        os.makedirs(directory, exist_ok=True)
        filename = f"{name}.star"
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            raise FileExistsError(f"API route already exists: '{path}'")

        content = f"""// ==============================================================================
// REST API Endpoint: {name}
// ==============================================================================

use Server
use Web

constant server = Server.app("{name}Service")

server.get("/api/{name}", function(req, res)
    variable response_data = {{
        "status": "success",
        "endpoint": "{name}",
        "timestamp": Time.now()
    }}
    res.json(response_data)
end)

server.post("/api/{name}", function(req, res)
    variable body = req.body
    res.status(201).json({{
        "status": "created",
        "received": body
    }})
end)

server.listen(8080)
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    @classmethod
    def make_model(cls, name: str, directory: str = "models") -> str:
        os.makedirs(directory, exist_ok=True)
        filename = f"{name}.star"
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            raise FileExistsError(f"Model file already exists: '{path}'")

        content = f"""// ==============================================================================
// Database Model: {name}
// ==============================================================================

use DB

class {name}
    property id = 0
    property created_at = ""

    function table()
        give back DB.table("{name.lower()}s")
    end

    function all()
        give back DB.table("{name.lower()}s").get()
    end

    function find(id)
        give back DB.table("{name.lower()}s").where("id", id).first()
    end
end
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
