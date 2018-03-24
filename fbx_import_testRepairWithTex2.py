#!BPY
import bpy
import bpy_extras.object_utils
from bpy.props import *
import sys
import os
import math
import numpy as np
import glob
import time
import random
from os.path import join as PathJoin
from mathutils import *

current_dir = os.getcwd()


#delete cube
cube = bpy.data.objects['Cube']
cube.select = True
bpy.ops.object.delete()

#import fbx
bpy.ops.import_scene.fbx(filepath='D:/GoogleDrive/BlenderFile/Testing/Models/Bip0123.fbx',automatic_bone_orientation=True)

fbx=bpy.context.scene.objects.active


#repair the rig
def repairRig(context):
 rig = bpy.context.object
 scn = bpy.context.scene
 eu  = rig.rotation_euler
 epsilon = 1e-2
 print(eu)
 if abs(eu.x) + abs(eu.y) + abs(eu.z) > epsilon:
  if scn.McpApplyObjectTransforms:
   bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
       
 vec = rig.scale - Vector((1,1,1))
 print(vec, vec.length)
 if vec.length > epsilon:
  if scn.McpApplyObjectTransforms:
   bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
 return rig  

fbx= repairRig(fbx)

#load animation
#bpy.ops.mcp.load_and_retarget(filepath='D:/MyBlender/Animation/walk.bvh')

#texture path/ load image for texture
texture_list=glob.glob("/Users/khairulanuarbinariff/Google Drive/realpeople-females/Textures/*.tga")


# for h in range(len(texture_list)):
# 	realpath = os.path.expanduser(texture_list[h])
# 	try:
# 	 img = bpy.data.images.load(realpath)
# 	except:
# 	 raise NameError("Cannot load image %s" % realpath)

# 	cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
# 	cTex.image = img

# 	#create new material from image texture
# 	mat = bpy.data.materials.new('TexMat')
# 	mtex = mat.texture_slots.add()
# 	mtex.texture = cTex #here is where the texture is append to material
# 	#settings for material 
# 	mtex.texture_coords = 'UV'
# 	mtex.use_map_color_diffuse = True 
# 	mtex.use_map_color_emission = True 
# 	mtex.emission_color_factor = 0.5
# 	mtex.use_map_density = True 
# 	mtex.mapping = 'FLAT' 



# 	#choose the mesh
# 	#dae = bpy.data.objects[len(bpy.data.objects)-1]
# 	dae=bpy.data.objects[2]
# 	dae.select = True
# 	bpy.context.scene.objects.active=dae
# 	#apply the texture to the mesh via material
# 	ob = bpy.context.object
# 	mesh = ob.data
# 	bpy.ops.object.material_slot_remove()#delete material if have usually model have at least 1 material
# 	mesh.materials.append(mat)

# 	#bpy.ops.context.render.alpha_mode = "TRANSPARENT"

# 	bpy.ops.render.render()
# 	Scene = bpy.context.scene

# 	img_fname = "/Users/khairulanuarbinariff/Desktop/gambar" + str(h) + ".png"
# 	bpy.data.images["Render Result"].save_render(filepath=img_fname)
