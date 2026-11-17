// 🌟 Star Native UI - Counter Application
// Authored in Haven (Heaven Language) Natural English Syntax
// Declarative Flutter Component Engine · 74,600+ UI Components
// Write Once. Run Everywhere (Desktop Canvas, Android SurfaceView, iOS MetalKit, WASM WebGPU, Terminal ANSI TUI)
// 100% Native · Zero JS Runtime Required

use Flutter
use Material
use Icons
use Colors

component FlutterCounter:
    remember count as 0

    to increment():
        increase count by 1
    end

    to decrement():
        decrease count by 1
    end

    render:
        Scaffold(
            appBar: AppBar(
                title: "🌟 Star Native UI · Haven Syntax",
                backgroundColor: Colors.indigo
            ),
            body: Center(
                child: Column(
                    children: [
                        Text("You have pushed the button this many times:"),
                        SizedBox(height: 8),
                        Text("Count: {count}"),
                        SizedBox(height: 20),
                        Row(
                            children: [
                                ElevatedButton("- Decrement", to ():
                                    decrease count by 1
                                end),
                                SizedBox(width: 16),
                                ElevatedButton("+ Increment", to ():
                                    increase count by 1
                                end)
                            ]
                        )
                    ]
                )
            ),
            floatingActionButton: FloatingActionButton(to ():
                increase count by 1
            end)
        )
    end
end

app CounterApp:
    FlutterCounter()
end
