shader_type canvas_item;

uniform vec3 target_point : hint_color; // World position of the point
uniform float max_distance = 50.0; // Maximum distance for the glitch effect

void fragment() {
    // Get the screen UV coordinates
    vec2 uv = FRAGCOORD.xy / SCREEN_PIXEL_SIZE;

    // Calculate the distance from the target point to the screen center
    vec2 screen_center = vec2(0.5, 0.5);
    float distance = length(screen_center - uv);

    // Map distance to glitch intensity
    float glitch_intensity = clamp(distance / max_distance, 0.0, 1.0);

    // Apply glitch effect with offset UVs
    vec2 glitch_offset = vec2(sin(TIME * 10.0 + uv.y * 20.0) * glitch_intensity, 0.0);
    vec2 new_uv = uv + glitch_offset;

    // Sample the screen texture
    COLOR = texture(SCREEN_TEXTURE, new_uv);
}
