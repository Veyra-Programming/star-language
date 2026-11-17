/**
 * Star Web Runtime & Reactive DOM Engine
 * Authoritative Reference: STAR_WEB.md & STAR_UI.md
 */

class StarWebRuntime {
    constructor() {
        this.memory = null;
        this.wasmInstance = null;
        this.rootContainer = document.getElementById("star-app-root") || document.body;
        this.uiTree = [];
        this.callbacks = new Map();
        this.nextCallbackId = 1;
    }

    readString(ptr, len) {
        if (!this.memory || len <= 0) return "";
        const bytes = new Uint8Array(this.memory.buffer, ptr, len);
        return new TextDecoder("utf-8").decode(bytes);
    }

    async init(wasmUrl = "app.wasm") {
        const importObject = {
            star_env: {
                star_show: (ptr, len) => {
                    const text = this.readString(ptr, len);
                    console.log("🌟 [Star]", text);
                    this.appendLog(text);
                },
                star_time_now: () => {
                    return performance.now();
                },
                star_ui_title: (ptr, len) => {
                    const text = this.readString(ptr, len);
                    this.uiTree.push({ type: "title", text });
                    this.reconcile();
                },
                star_ui_text: (ptr, len) => {
                    const text = this.readString(ptr, len);
                    this.uiTree.push({ type: "text", text });
                    this.reconcile();
                },
                star_ui_button: (ptr, len, callbackId) => {
                    const text = this.readString(ptr, len);
                    this.uiTree.push({ type: "button", text, callbackId });
                    this.reconcile();
                },
                star_ui_column: (count) => {
                    // Container marker
                    this.reconcile();
                },
                star_ui_card: (count) => {
                    this.reconcile();
                }
            }
        };

        try {
            const response = await fetch(wasmUrl);
            const bytes = await response.arrayBuffer();
            const results = await WebAssembly.instantiate(bytes, importObject);
            this.wasmInstance = results.instance;
            this.memory = this.wasmInstance.exports.memory;

            // Execute main
            if (this.wasmInstance.exports.main) {
                this.wasmInstance.exports.main();
            }
        } catch (err) {
            console.error("Failed to initialize Star Web Runtime:", err);
            this.appendLog("Runtime Error: " + err.message, true);
        }
    }

    reconcile() {
        if (!this.rootContainer) return;
        const mainContainer = document.getElementById("star-ui-container");
        if (!mainContainer) return;

        mainContainer.innerHTML = "";
        for (const item of this.uiTree) {
            if (item.type === "title") {
                const el = document.createElement("h1");
                el.className = "star-title";
                el.textContent = item.text;
                mainContainer.appendChild(el);
            } else if (item.type === "text") {
                const el = document.createElement("p");
                el.className = "star-text";
                el.textContent = item.text;
                mainContainer.appendChild(el);
            } else if (item.type === "button") {
                const el = document.createElement("button");
                el.className = "star-button";
                el.textContent = item.text;
                el.onclick = () => {
                    if (this.wasmInstance && this.wasmInstance.exports.star_dispatch_event) {
                        this.wasmInstance.exports.star_dispatch_event(item.callbackId);
                    }
                };
                mainContainer.appendChild(el);
            }
        }
    }

    appendLog(msg, isError = false) {
        const consoleEl = document.getElementById("star-console-output");
        if (consoleEl) {
            const line = document.createElement("div");
            line.className = isError ? "star-log-error" : "star-log-line";
            line.textContent = msg;
            consoleEl.appendChild(line);
            consoleEl.scrollTop = consoleEl.scrollHeight;
        }
    }
}

// Auto-boot on window load
window.addEventListener("DOMContentLoaded", () => {
    window.starRuntime = new StarWebRuntime();
    window.starRuntime.init("app.wasm");
});
