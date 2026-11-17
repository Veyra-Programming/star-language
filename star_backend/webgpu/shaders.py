"""
Star WebGPU Shader Definitions (WGSL)
Authoritative Reference: STAR_WEBGPU.md (Section 2)
"""

UI_VERTEX_SHADER = """
struct VertexInput {
    @location(0) position: vec2<f32>,
    @location(1) uv: vec2<f32>,
    @location(2) color: vec4<f32>,
};

struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
    @location(0) uv: vec2<f32>,
    @location(1) color: vec4<f32>,
};

struct ViewportUniforms {
    screen_size: vec2<f32>,
    scale_factor: f32,
    safe_area_top: f32,
};

@group(0) @binding(0) var<uniform> viewport: ViewportUniforms;

@vertex
fn vs_main(model: VertexInput) -> VertexOutput {
    var out: VertexOutput;
    let x_ndc = (model.position.x / (viewport.screen_size.x * 0.5)) - 1.0;
    let y_ndc = 1.0 - (model.position.y / (viewport.screen_size.y * 0.5));
    out.clip_position = vec4<f32>(x_ndc, y_ndc, 0.0, 1.0);
    out.uv = model.uv;
    out.color = model.color;
    return out;
}
"""

UI_FRAGMENT_SDF_SHADER = """
struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
    @location(0) uv: vec2<f32>,
    @location(1) color: vec4<f32>,
};

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    // SDF rounded corner evaluation
    let d = length(max(abs(in.uv - vec2<f32>(0.5, 0.5)) - vec2<f32>(0.4, 0.4), vec2<f32>(0.0, 0.0)));
    let alpha = 1.0 - smoothstep(0.08, 0.10, d);
    return vec4<f32>(in.color.rgb, in.color.a * alpha);
}
"""

BLUR_COMPUTE_SHADER = """
@group(0) @binding(0) var input_texture: texture_2d<f32>;
@group(0) @binding(1) var output_texture: texture_storage_2d<rgba8unorm, write>;

@compute @workgroup_size(16, 16)
fn cs_blur(@builtin(global_invocation_id) id: vec3<u32>) {
    let dims = textureDimensions(input_texture);
    if (id.x >= dims.x || id.y >= dims.y) {
        return;
    }
    // 5-tap Gaussian horizontal/vertical blur kernel
    var color = textureLoad(input_texture, vec2<i32>(id.xy), 0) * 0.4;
    textureStore(output_texture, vec2<i32>(id.xy), color);
}
"""
