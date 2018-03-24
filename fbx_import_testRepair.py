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

#full_path_to_dae = PathJoin(current_dir, "Models", "dae_human3.dae")<---‚±‚±‚ª–â‘è‚©‚à‚¹‚µ‚È‚¢
#•’Ê‚É@full_path_to_dae='D:\MyBlender\TestDae\dae_human.dae' import@‚Å‚«‚é‚æ

#delete cube
cube = bpy.data.objects['Cube']
cube.select = True
bpy.ops.object.delete()

#import fbx
bpy.ops.import_scene.fbx(filepath='D:/Unity/boom/Assets/Yurowm/Characters/Sporty Girl/SportyGirl.fbx',automatic_bone_orientation=True)


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
bpy.ops.mcp.load_and_retarget(filepath='D:/MyBlender/Animation/walk.bvh')


realpath = os.path.expanduser('D:/MyBlender/PyScript/640px-Code_Snippets_color.png')
try:
 img = bpy.data.images.load(realpath)
except:
 raise NameError("Cannot load image %s" % realpath)

cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
cTex.image = img


mat = bpy.data.materials.new('TexMat')
mtex = mat.texture_slots.add()
mtex.texture = cTex
mtex.texture_coords = 'UV'
mtex.use_map_color_diffuse = True 
mtex.use_map_color_emission = True 
mtex.emission_color_factor = 0.5
mtex.use_map_density = True 
mtex.mapping = 'FLAT' 


#ob = bpy.context.object
#me = ob.data
#me.materials.append(mat)