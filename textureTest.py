import bpy, os
 
def run(origin):
    # Load image file. Change here if the snippet folder is 
    # not located in you home directory.
    realpath = os.path.expanduser('D:/MyBlender/PyScript/640px-Code_Snippets_color.png')
    try:
        img = bpy.data.images.load(realpath)
    except:
        raise NameError("Cannot load image %s" % realpath)
 
    # Create image texture from image
    cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    cTex.image = img
 
    # Create procedural texture 
    sTex = bpy.data.textures.new('BumpTex', type = 'STUCCI')
    sTex.noise_basis = 'BLENDER_ORIGINAL' 
    sTex.noise_scale = 0.25 
    sTex.noise_type = 'SOFT_NOISE' 
    sTex.saturation = 1 
    sTex.stucci_type = 'PLASTIC' 
    sTex.turbulence = 5 
 
    # Create blend texture with color ramp
    # Don't know how to add elements to ramp, so only two for now
    bTex = bpy.data.textures.new('BlendTex', type = 'BLEND')
    bTex.progression = 'SPHERICAL'
    bTex.use_color_ramp = True
    ramp = bTex.color_ramp
    values = [(0.6, (1,1,1,1)), (0.8, (0,0,0,1))]
    for n,value in enumerate(values):
        elt = ramp.elements[n]
        (pos, color) = value
        elt.position = pos
        elt.color = color
 
    # Create material
    mat = bpy.data.materials.new('TexMat')
 
    # Add texture slot for color texture
    mtex = mat.texture_slots.add()
    mtex.texture = cTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.use_map_color_emission = True 
    mtex.emission_color_factor = 0.5
    mtex.use_map_density = True 
    mtex.mapping = 'FLAT' 
 
    # Add texture slot for bump texture
    mtex = mat.texture_slots.add()
    mtex.texture = sTex
    mtex.texture_coords = 'ORCO'
    mtex.use_map_color_diffuse = False
    mtex.use_map_normal = True 
    #mtex.rgb_to_intensity = True
 
    # Add texture slot 
    mtex = mat.texture_slots.add()
    mtex.texture = bTex
    mtex.texture_coords = 'UV'
    mtex.use_map_color_diffuse = True 
    mtex.diffuse_color_factor = 1.0
    mtex.blend_type = 'MULTIPLY'
 
    # Create new cube and give it UVs
    bpy.ops.mesh.primitive_cube_add(location=origin)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')
 
    # Add material to current object
    ob = bpy.context.object
    me = ob.data
    me.materials.append(mat)
 
    return
 
if __name__ == "__main__":
    run((0,0,0))