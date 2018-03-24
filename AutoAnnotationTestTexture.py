#!BPY
import bpy
import bpy_extras.object_utils
from bpy.props import *
from mathutils import *
import sys
import os
import math
import numpy as np
import glob
import time
import random
import csv
from random import randint
from os.path import join as PathJoin

time1 = time.clock()

# ============================================================
# General Settings
# ============================================================

OS_Windows = True
# OS_Windows = False

CurDir = os.getcwd()

old_file_clear = True

# ============================================================
# Scene Settings
# ============================================================

scene = bpy.data.scenes["Scene"]
scene.view_settings.gamma = 1.0
scene.sequencer_colorspace_settings.name = "Linear"

camera = scene.camera

# ============================================================
# Light Settings
# ============================================================

scene.world.light_settings.use_environment_light = False
scene.world.light_settings.environment_energy = 0.0

scene.world.light_settings.use_ambient_occlusion = True
scene.world.light_settings.ao_factor = 1.0

# ============================================================
# Render Settings
# ============================================================

# resolution
Res_x = 640
Res_y = 480
Res_p = 100

renderSetting = scene.render
renderSetting.resolution_x = Res_x
renderSetting.resolution_y = Res_y
renderSetting.resolution_percentage = Res_p

# renderSetting.use_motion_blur = True
# renderSetting.motion_blur_samples = 1
# renderSetting.motion_blur_shutter = 0.5

# ============================================================
# Path Settings to Human Model and Motion Capture
# ============================================================

#human_model_list = glob.glob("Models/Sample_mhx2_08models/*.mhx2")
human_model_list = glob.glob("D:/GoogleDrive/BlenderFile/Testing/Models/Bip01.fbx")

print(human_model_list)

path_to_bvh_dir = "D:/GoogleDrive/BlenderFile/Testing/"
bvh_dir_list = ["Bvh"]
all_bvh_file_list = []
for bvh_dir in bvh_dir_list:
	bvh_files = glob.glob(PathJoin(path_to_bvh_dir, bvh_dir, "*.bvh"))
	all_bvh_file_list.extend(bvh_files)

# ============================================================
# Classified Directory Name
# ============================================================

class_list = ["class00", "class01", "class02", "class03", "class04", "class05", "class06", "class07", "class08"]

# ============================================================
# Delete Default Cube
# ============================================================

cube = bpy.data.objects["Cube"]
cube.select = True
cube.location = (2, -2, 2)
cube.scale = (0.3, 0.3, 0.3)
bpy.ops.object.delete()
cube.select = False

# ============================================================
# Random Parameters
# ============================================================

scale_h_list = [0.30, 0.32, 0.34, 0.36, 0.38]
AO_Factor_list = [1.0, 1.2, 1.4, 1.6]
LampEnergy_list = [1.0, 1.2, 1.4, 1.6]

rot_x_list = range(-25, 26, 10)
rot_z_list = range(0, 360, 30)

# ============================================================
# Camera Settings
# ============================================================

# cam_position = (-0.2, 17.7, 15.0)
# (cam_rx, cam_ry, cam_rz) = (60, 0, 180)

# cam_position = (0.0, 20.0, 10.0)
# (cam_rx, cam_ry, cam_rz) = (60, 0, 180)

cam_position = (1.7, -7.3, 2.82)
(cam_rx, cam_ry, cam_rz) = (60, 0, 0)


scene.camera.rotation_mode = "XYZ"
scene.camera.rotation_euler[0] = cam_rx*(math.pi/180.0)
scene.camera.rotation_euler[1] = cam_ry*(math.pi/180.0)
scene.camera.rotation_euler[2] = cam_rz*(math.pi/180.0)
scene.camera.location = cam_position

# ============================================================
# Class Object and Function Definition
# ============================================================

class HumanModel:

	def __init__(self, path_mhx2):

		#full_path_to_mhx2 = PathJoin(CurDir, path_mhx2)
		#bpy.ops.import_scene.makehuman_mhx2(filepath=full_path_to_mhx2)


		#importing fbx
		full_path_to_mhx2 = path_mhx2
		bpy.ops.import_scene.fbx(filepath=full_path_to_mhx2,automatic_bone_orientation=True)

		
		#put line for import fbx with repair bone
		fbx=bpy.context.scene.objects.active
		fbx=repairRig(fbx)

		# def repairRig(context):

 	# 		rig = bpy.context.object
 	# 		scn = bpy.context.scene
 	# 		eu  = rig.rotation_euler
 	# 		epsilon = 1e-2
 	# 		print(eu)
 	# 		if abs(eu.x) + abs(eu.y) + abs(eu.z) > epsilon:
  # 		 	 if scn.McpApplyObjectTransforms:
  #  		 	  bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
       
 	# 		vec = rig.scale - Vector((1,1,1))
 	# 		print(vec, vec.length)
 	# 		if vec.length > epsilon:
  # 		 	 if scn.McpApplyObjectTransforms:
  #  		 	  bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
 	# 		return rig  

 	


		if (OS_Windows == True):
			fname = path_mhx2.split("\\")[-1]
		else:
			fname = path_mhx2.split("/")[-1]

		key, ext = os.path.splitext(fname)
		self.obj = bpy.data.objects[0]

	def retarget_bvh(self, path_bvh):
		#full_path_to_bvh = PathJoin(CurDir, path_bvh)
		#bpy.ops.mcp.load_and_retarget(filepath=full_path_to_bvh)
		bpy.ops.mcp.load_and_retarget(filepath=path_bvh)

	def set_human_scale(self, scale_h=0.15):
		self.obj.scale = (scale_h, scale_h, scale_h)

	def set_human_rotation(self, rx=0, ry=0, rz=0):
		self.rx = rx
		self.ry = ry
		self.rz = rz

		rad_rx = (math.pi/180.0) * self.rx
		rad_ry = (math.pi/180.0) * self.ry
		rad_rz = (math.pi/180.0) * self.rz

		self.obj.rotation_mode = "XYZ"
		self.obj.rotation_euler = (rad_rx, rad_ry, rad_rz)
		self.obj.select = False

class LampObj:

	def __init__(self):
		self.obj = bpy.data.objects["Lamp"]

	def set_lamp_type(self, lamp_type="POINT"):
		self.lamp_type = lamp_type
		self.obj.data.type = self.lamp_type
	
	def set_lamp_energy(self, lamp_energy=2.0):
		self.lamp_energy = lamp_energy
		bpy.data.lamps["Lamp"].energy = self.lamp_energy

def delete_old_files():

	for dir_name in class_list:

		gt_files = glob.glob(PathJoin(CurDir, "GtFiles", dir_name, "*.txt"))
		ub5_files = glob.glob(PathJoin(CurDir, "UpperBody5pt", dir_name, "*.csv"))
		rec_files = glob.glob(PathJoin(CurDir, "Rectangle", dir_name, "*.csv"))
		image_files = glob.glob(PathJoin(CurDir, "RenderResult", dir_name, "*.png"))

		old_files = gt_files+ub5_files+rec_files+image_files

		for x in old_files:
			os.remove(x)

def get_camera_3Dcoord(human, bone_name, edge="head"):

	if edge == "tail":
		bone_loc = human.obj.pose.bones[bone_name].tail
	else:
		bone_loc = human.obj.pose.bones[bone_name].head

	world_loc = human.obj.matrix_world * bone_loc

	coord_3D = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_loc)

	coord_x = round(coord_3D[0]*Res_x*(Res_p/100))
	coord_y = round(coord_3D[1]*Res_y*(Res_p/100))
	coord_z = coord_3D[2]

	coord_3D = np.array([coord_x, coord_y, coord_z])

	return coord_3D

def get_world_3Dcoord(human, bone_name, edge="head"):

	if edge == "tail":
		bone_loc = human.obj.pose.bones[bone_name].tail
	else:
		bone_loc = human.obj.pose.bones[bone_name].head

	world_loc = np.array(human.obj.matrix_world * bone_loc)

	return world_loc

def Annotation_transform(human, iteration):


#Need to change the Bone name
#put if utk fbx
	Head_camera = get_camera_3Dcoord(human, "Head", "tail")
	ArmL_camera = get_camera_3Dcoord(human, "LeftArm")
	ArmR_camera = get_camera_3Dcoord(human, "RightArm")
	LegL_camera = get_camera_3Dcoord(human, "LeftUpLeg")
	LegR_camera = get_camera_3Dcoord(human, "RightUpLeg")

	UpperBody5pt_3D = np.array([LegR_camera, ArmR_camera, Head_camera, 
		ArmL_camera, LegL_camera])

	UB5_fname = prefix+"UpperBody5pt_"+str(iteration).zfill(digits)+".csv"
	full_path_to_UB5 = PathJoin(CurDir, "UpperBody5pt", class_list[classNum], UB5_fname)
	np.savetxt(full_path_to_UB5, UpperBody5pt_3D, fmt="%0.5f", delimiter=",")

	print("\n< UpperBody5pt >")
	print(UpperBody5pt_3D)

	UpperBody5pt_2D = UpperBody5pt_3D[:,:2]

	head_center_camera = (UpperBody5pt_2D[1]+UpperBody5pt_2D[3]+UpperBody5pt_2D[2])/3.0
	shoulder_center_camera = (UpperBody5pt_2D[1]+UpperBody5pt_2D[3]+UpperBody5pt_2D[0]+UpperBody5pt_2D[4])/4.0

	# estimate the size of head using the distance between head_center and (head, both arrms). 
	size_top = np.linalg.norm(UpperBody5pt_2D[2]-head_center_camera)
	size_left = np.linalg.norm(UpperBody5pt_2D[1]-head_center_camera)
	size_right = np.linalg.norm(UpperBody5pt_2D[3]-head_center_camera)

	height = width = round(2*max(size_top, size_left, size_right))

	xpos = round(head_center_camera[0] - width/2.0)
	ypos = round(head_center_camera[1] - height/2.0)

	return xpos, ypos, width, height

def create_Gt_file(human, iteration, classNum):

	[xpos, ypos, width, height] = Annotation_transform(human, iteration)
	XX = xpos
	YY = Res_y-(ypos+height)

	Gt_fname = prefix+"img_"+str(iteration).zfill(digits)+".txt"
	full_path_to_Gt = PathJoin(CurDir, "GtFiles", class_list[classNum], Gt_fname)

	fp = open(full_path_to_Gt, "w")
	fp.write("% bbGt version=3\n")
	fp.write("person %d %d %d %d 0 0 0 0 0 0 0\n"%(XX, YY, width, height))
	fp.close()

	Rectangle = [xpos, ypos, width, height]

	rec_fname = prefix+"Rectangle_"+str(iteration).zfill(digits)+".csv"
	full_path_to_rec = PathJoin(CurDir, "Rectangle", class_list[classNum], rec_fname)
	np.savetxt(full_path_to_rec, Rectangle, fmt="%0.5f", delimiter=",")

	print("\n< Rectangle >")
	print(Rectangle)

def rendering(iteration, human, image_counter):

	angle1 = Label_RIP(human)

	theta1_L, theta1_R, theta2_L, theta2_R = Label_Arm(human)
	angle2 = int((theta2_L+theta2_R)/2.0)

	# LABEL1
	if   (abs(angle1)<= 10): label1 = 0
	elif (abs(angle1)<= 30): label1 = 1
	else: label1 = 2

	# LABEL2
	if   (angle2>= 40): label2 = 0
	elif (angle2>=  0): label2 = 1
	else: label2 = 2

	# classNum = 0
	# classNum = 3*label1 + label2
	classNum = label2
	RenderResult_dir = class_list[classNum]

	if (classNum == 2):
		image_counter += 1

	renderSetting.alpha_mode = "TRANSPARENT"
	bpy.ops.render.render()

	img_fname = prefix+"img_"+str(iteration).zfill(digits)+".png"
	# img_fname = str(angle4)+".png"
	full_path_to_img = PathJoin(CurDir, "RenderResult", RenderResult_dir, img_fname)
	bpy.data.images["Render Result"].save_render(filepath=full_path_to_img)

	return classNum, image_counter

def Label_Arm(human):

	Head_world = get_world_3Dcoord(human, "Head", "tail")
	ArmL_world = get_world_3Dcoord(human, "LeftArm")
	ArmR_world = get_world_3Dcoord(human, "RightArm")
	LegL_world = get_world_3Dcoord(human, "LeftUpLeg")
	LegR_world = get_world_3Dcoord(human, "RightUpLeg")
	# ElbL_world = get_world_3Dcoord(human, "LeftArmRoll", "tail")
	# ElbR_world = get_world_3Dcoord(human, "RightArmRoll", "tail")
	ElbL_world = get_world_3Dcoord(human, "LeftArm", "tail")
	ElbR_world = get_world_3Dcoord(human, "RightArm", "tail")


	# ================================================================================
	# Lable 1 : The angle of arms against normal vector of Plane A. 
	# (Plane A : the plane determined by the 3 points(head_center, LegL, LegR). )
	#
	# Label 2 : The angle of arms against body axis
	# ================================================================================

	head_center_world = (Head_world+ArmL_world+ArmR_world)/3.0
	shoulder_mid_world = (ArmL_world+ArmR_world)/2.0
	shoulder_center_world = (ArmL_world+ArmR_world+LegL_world+LegR_world)/4.0

	vec_L = np.array(LegL_world-shoulder_mid_world)
	vec_R = np.array(LegR_world-shoulder_mid_world)
	normal_vec = np.cross(vec_R, vec_L)

	# inner product
	Dot1_L = np.dot(ElbL_world-ArmL_world, normal_vec)
	Dot1_R = np.dot(ElbR_world-ArmR_world, normal_vec)
	Dot2_L = np.dot(ElbL_world-ArmL_world, shoulder_center_world-head_center_world)
	Dot2_R = np.dot(ElbR_world-ArmR_world, shoulder_center_world-head_center_world)
	
	# norm
	Len_L = np.linalg.norm(np.array(ElbL_world-ArmL_world))
	Len_R = np.linalg.norm(np.array(ElbR_world-ArmR_world))
	Len_NV = np.linalg.norm(np.array(normal_vec))
	Len_SH = np.linalg.norm(np.array(shoulder_center_world-head_center_world))

	# angle
	theta1_L = (Dot1_L/(Len_L*Len_NV))*360/(2*math.pi)
	theta1_R = (Dot1_R/(Len_R*Len_NV))*360/(2*math.pi)
	theta2_L = (Dot2_L/(Len_L*Len_SH))*360/(2*math.pi)
	theta2_R = (Dot2_R/(Len_R*Len_SH))*360/(2*math.pi)

	# print("\n< Label Arm >")
	# print("theta1_L = "+str(theta1_L))
	# print("theta1_R = "+str(theta1_R))
	# print("theta2_L = "+str(theta2_L))
	# print("theta2_R = "+str(theta2_R))

	return theta1_L, theta1_R, theta2_L, theta2_R

def Label_Body(human):

	Head_camera = get_camera_3Dcoord(human, "Head", "tail")
	ArmL_camera = get_camera_3Dcoord(human, "LeftArm")
	ArmR_camera = get_camera_3Dcoord(human, "RightArm")
	LegL_camera = get_camera_3Dcoord(human, "LeftUpLeg")
	LegR_camera = get_camera_3Dcoord(human, "RightUpLeg")

	head_center_camera = (Head_camera+ArmL_camera+ArmR_camera)/3.0
	shoulder_center_camera = (ArmL_camera+ArmR_camera+LegL_camera+LegR_camera)/4.0

	Head_world = get_world_3Dcoord(human, "Head", "tail")
	ArmL_world = get_world_3Dcoord(human, "LeftArm")
	ArmR_world = get_world_3Dcoord(human, "RightArm")
	LegL_world = get_world_3Dcoord(human, "LeftUpLeg")
	LegR_world = get_world_3Dcoord(human, "RightUpLeg")

	head_center_world = (Head_world+ArmL_world+ArmR_world)/3.0
	shoulder_center_world = (ArmL_world+ArmR_world+LegL_world+LegR_world)/4.0

	# ================================================================================
	# Calculated theta is the angle between camera plane and the vector of body axis.
	# ================================================================================

	norm_body_3D = np.linalg.norm(shoulder_center_world-head_center_world)
	norm_body_2D = shoulder_center_camera[2]-head_center_camera[2]

	theta = math.acos(norm_body_2D/norm_body_3D)*360/(2*math.pi)

	return int(theta)

def Label_RIP(human):

	Head_camera = get_camera_3Dcoord(human, "Head", "tail")
	ArmL_camera = get_camera_3Dcoord(human, "LeftArm")
	ArmR_camera = get_camera_3Dcoord(human, "RightArm")
	LegL_camera = get_camera_3Dcoord(human, "LeftUpLeg")
	LegR_camera = get_camera_3Dcoord(human, "RightUpLeg")

	head_center_camera = (Head_camera+ArmL_camera+ArmR_camera)/3.0
	shoulder_center_camera = (ArmL_camera+ArmR_camera+LegL_camera+LegR_camera)/4.0

	Head_camera_2d = Head_camera[:2]
	shoulder_center_camera_2D = shoulder_center_camera[:2]

	dist = np.linalg.norm(Head_camera_2d-shoulder_center_camera_2D)
	delta_x = Head_camera[0]-shoulder_center_camera[0]

	[x1, y1] = Head_camera_2d
	[x2, y2] = shoulder_center_camera_2D

	if ((x1 <= x2) and (y1 <= y2)):
		rip = -180-(math.asin(delta_x/dist)*360/(2*math.pi))
	elif ((x1 >= x2) and (y1 <= y2)):
		rip = 180 - (math.asin(delta_x/dist)*360/(2*math.pi))
	else:
		rip = (math.asin(delta_x/dist)*360/(2*math.pi))

	return int(rip)

def Label_ROP(human):

	ArmL_world = get_world_3Dcoord(human, "LeftArm")
	ArmR_world = get_world_3Dcoord(human, "RightArm")
	LegL_world = get_world_3Dcoord(human, "LeftUpLeg")
	LegR_world = get_world_3Dcoord(human, "RightUpLeg")

	posL_world = (ArmL_world+LegL_world)/2.0
	posR_world = (ArmR_world+LegR_world)/2.0

	delta_x = posL_world[0] - posR_world[0]
	delta_y = posL_world[1] - posR_world[1]

	xy_dist = math.sqrt(delta_x*delta_x+delta_y*delta_y)

	if delta_y > 0:
		rop = -(180-math.acos(delta_x/xy_dist)*360/(2*math.pi))
	else:
		rop = 180-math.acos(delta_x/xy_dist)*360/(2*math.pi)

	return int(rop)
	
def delete_human():

	for item in bpy.context.scene.objects:
	    if item.type == 'MESH':
	        bpy.context.scene.objects.unlink(item)
	for item in bpy.data.objects:
	    if item.type == 'MESH':
	        bpy.data.objects.remove(item)
	for item in bpy.data.meshes:
	    bpy.data.meshes.remove(item)
	for item in bpy.data.materials:
	    bpy.data.materials.remove(item)

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

def ApplyTex(texture):

 	
	realpath = os.path.expanduser(texture_list[texture])
	try:
	 img = bpy.data.images.load(realpath)
	except:
	 raise NameError("Cannot load image %s" % realpath)

	cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
	cTex.image = img

	#create new material from image texture
	mat = bpy.data.materials.new('TexMat')
	mtex = mat.texture_slots.add()
	mtex.texture = cTex #here is where the texture is append to material
	#settings for material 
	mtex.texture_coords = 'UV'
	mtex.use_map_color_diffuse = True 
	mtex.use_map_color_emission = True 
	mtex.emission_color_factor = 0.5
	mtex.use_map_density = True 
	mtex.mapping = 'FLAT' 

	


	#choose the mesh
	#dae = bpy.data.objects[len(bpy.data.objects)-1]
	dae=bpy.data.objects[2]
	dae.select = True
	bpy.context.scene.objects.active=dae
	#apply the texture to the mesh via material
	ob = bpy.context.object
	mesh = ob.data
	bpy.ops.object.material_slot_remove()#delete material if have usually model have at least 1 material
	mesh.materials.append(mat)

	#bpy.ops.context.render.alpha_mode = "TRANSPARENT"







def get_blender_frame_number(path_bvh):

	blender_frame_rate = 24

	fid = open(PathJoin(CurDir, path_bvh))
	lines = fid.readlines()
	fid.close()

	for line in lines:

		if line.find('Frames') >= 0:
			str1 = line.rstrip("\r\n")
			str2 = str1.lstrip("Frames: ")
			bvh_frame_number = int(str2)

		if line.find('Frame Time') >= 0:
			str1 = line.rstrip("\r\n")
			str2 = str1.lstrip("Frame Time: ")
			bvh_frame_time = float(str2)

	blender_frame_number = int(bvh_frame_number*bvh_frame_time*blender_frame_rate)

	if blender_frame_number >= 250:
		blender_frame_number = 250

	return blender_frame_number


if __name__ == "__main__":

	time2 = time.clock()

	# ============================================================
	# Make BVH Frames List that matches some conditions. 
	# ============================================================

	# human = HumanModel(path_mhx2=human_model_list[0])
	
	# selected_bvh_frame_list = []

	# for bvh_file in all_bvh_file_list:

	# 	frameNum = get_blender_frame_number(path_bvh=bvh_file)
	# 	human.retarget_bvh(path_bvh=bvh_file)

	# 	for frame in range(frameNum):

	# 		scene.frame_set(frameNum)

	# 		# ========================================
	# 		# Discript Conditions Here
	# 		# ========================================

	# 		theta1_L, theta1_R, theta2_L, theta2_R = Label_Arm(human)
	# 		angle_arm = (theta2_L+theta2_R)/2.0

	# 		if angle_arm < 0:

	# 			bvh_frame = [bvh_file, frameNum]
	# 			selected_bvh_frame_list.append(bvh_frame)

	# delete_human()

	# time4 = time.clock()

	# timer3 = time4-time2
	# minutes3 = math.floor(timer3/60)
	# seconds3 = timer3%60	

	# print("========================================")
	# print("Successfully Made BVH Files List")
	# print("Total Frame Number : "+str(len(selected_bvh_frame_list)))
	# print("Processing Time : "+str(minutes3)+"min "+str(seconds3)+"sec")
	# print("========================================")

	# ============================================================

	#f = open("123.txt", "rb")
	#lines = f.readlines()
	#f.close()

	prefix = "z_"
	digits = 6

	# selected_bvh_frame_list = []
	# for line in lines:
	# 	bvh, frame = str(line).split(" ")
	# 	bvh = PathJoin(CurDir, bvh[2:])
	# 	frame = int(frame[0:3])
	# 	selected_bvh_frame_list.append([bvh, int(frame)])



	# ============================================================

	if (old_file_clear == True):
		delete_old_files()

	iteration = 1469
	lamp1 = LampObj()

	print(human_model_list)
	#for fbx
	texture_list=glob.glob("D:/GoogleDrive/BlenderFile/realpeople-females/Textures/*.tga")
	textureLen=len(texture_list)
	textureId=randint(0,textureLen)
	#print(texture_list)
	print("textureLen=",textureLen)
	

	for h in range(len(human_model_list)):

		textureId=randint(0,textureLen)
		ImageCounter = 0
		Reps = 10
		#human = HumanModel(path_mhx2=human_model_list[h])
		human = HumanModel(path_mhx2=human_model_list[h])
		ApplyTex(textureId)
		while ImageCounter < Reps:

			random.seed(iteration)

			AO_Factor = random.choice(AO_Factor_list)
			scene.world.light_settings.ao_factor = AO_Factor

			# bvh_frame = random.choice(selected_bvh_frame_list)
			#human.retarget_bvh(path_bvh=bvh_frame[0])
			bpy.context.scene.objects.active=bpy.data.objects[0]				
			human.retarget_bvh(path_bvh="D:/GoogleDrive/BlenderFile/Testing/Bvh/123.bvh")

			frameNum = get_blender_frame_number(path_bvh="D:/GoogleDrive/BlenderFile/Testing/Bvh/123.bvh")
			frame_list = range(frameNum)
			selected_frames = random.sample(frame_list, 5)
			print(selected_frames)

			#print(bvh_file)

			scale_h = random.choice(scale_h_list)
			rot_x = random.choice(rot_x_list)
			rot_z = random.choice(rot_z_list)


			
			print("scale_h = "+str(scale_h))
			print("rot_x = "+str(rot_x))
			print("rot_z = "+str(rot_z))
			
			#human.set_human_scale(scale_h)
			
			human.set_human_rotation(rx=rot_x, rz=rot_z)

			LampEnergy = random.choice(LampEnergy_list)
			print("Lamp Energy : "+str(LampEnergy))
			lamp1.set_lamp_energy(lamp_energy=LampEnergy)

			#setting for frame
			scene.frame_set(125)

			print("\n\n<---------- iteration "+str(iteration)+" ---------->")

			rip = Label_RIP(human)
			body_axis = Label_Body(human)

			if (abs(rip) <= 30) and (50 <= body_axis) and (body_axis <= 100):

				classNum, ImageCounter = rendering(iteration, human, ImageCounter)
				create_Gt_file(human, iteration, classNum)
				print("Image Counter : "+str(ImageCounter))

			iteration += 1

			if ImageCounter == Reps:
				break

		#delete_human()


	time3 = time.clock()
	timer1 = int(time2-time1)
	minutes1 = math.floor(timer1/60)
	seconds1 = timer1%60
	timer2 = int(time3-time2)
	minutes2 = math.floor(timer2/60)
	seconds2 = timer2%60
	print("\nIt takes "+str(minutes1)+"min "+str(seconds1)+"sec for Pre-process.")
	print("It takes "+str(minutes2)+"min "+str(seconds2)+"sec for process of FOR LOOP.")
	print("(The numbe of rendering : "+str(iteration)+")\n")

	sys.exit()
