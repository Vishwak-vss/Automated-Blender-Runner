import bpy

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# 1. Device Setup (Robust Enable)
scene.cycles.device = 'GPU'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.get_devices()

    # Try enabling available compute backends in priority order
    for device_type in ['OPTIX', 'CUDA', 'HIP', 'METAL']:
        try:
            prefs.compute_device_type = device_type
            for dev in prefs.devices:
                dev.use = True
            break
        except Exception:
            continue
except Exception as e:
    print(f"[Warning] Could not configure GPU device via API: {e}")

# 2. Denoising Fix (Handles Blender 3.x, 4.x, and 5.x property names)
scene.cycles.use_denoising = True

if hasattr(scene.cycles, 'use_preview_denoising'):
    scene.cycles.use_preview_denoising = False
elif hasattr(scene.cycles, 'use_preview_denoise'):
    setattr(scene.cycles, 'use_preview_denoise', False)

# Set OptiX denoiser if available, fallback to OPENIMAGEDENOISE
try:
    scene.cycles.denoiser = 'OPTIX'
except TypeError:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# 3. Adaptive Sampling & Sample Limits
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.015  # Stops early on clean/flat areas
scene.cycles.samples = 256              # Cut from 4096 to 256

# 4. Ray Bounces Optimization
scene.cycles.max_bounces = 6
scene.cycles.diffuse_bounces = 3
scene.cycles.glossy_bounces = 4
scene.cycles.transmission_bounces = 6
scene.cycles.volume_bounces = 0
scene.cycles.transparent_max_bounces = 8

# 5. Fast GI & Clamping
scene.cycles.sample_clamp_indirect = 10.0
scene.cycles.use_fast_gi = True
scene.cycles.fast_gi_method = 'ADD'

# 6. Performance Options
scene.render.use_persistent_data = True