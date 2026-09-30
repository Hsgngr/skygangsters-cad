"""Render the actual STEP-derived carrier geometry."""
import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parent/'candidates/carrier_v4'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True
s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world.color=(.3,.3,.3);s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-2.5
def mat(name,color):
    rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Roughness'].default_value=.5;return m
objects={}
for row in json.loads((ROOT/'scene.json').read_text()):
    bpy.ops.wm.stl_import(filepath=str(ROOT/row['file']),global_scale=.001)
    o=bpy.context.object;o.name=row['name'];o.data.materials.append(mat(o.name,row['color']));objects[o.name]=o
for name,pos,power,size in [('Key',(.1,-.3,.35),28,.35),('Fill',(-.25,.05,.2),16,.3),('Rim',(.2,.3,.35),35,.3)]:
    light=bpy.data.lights.new(name,'AREA');light.energy=power;light.size=size
    obj=bpy.data.objects.new(name,light);s.collection.objects.link(obj);obj.location=pos
    obj.rotation_euler=(Vector((0,0,0))-obj.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.mesh.primitive_plane_add(size=20,location=(0,0,-.13));ground=bpy.context.object;ground.data.materials.append(mat('Background','#D9DEDF'))
data=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',data);s.collection.objects.link(cam);s.camera=cam;data.type='ORTHO'
def render(name,pos,target,scale):
    cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    data.ortho_scale=scale;s.render.filepath=str(ROOT/(name+'.png'));bpy.ops.render.render(write_still=True)
render('01_carrier_with_user_pump',(.23,-.36,.23),(0,0,-.045),.28)
for name,o in objects.items():
    if name.startswith('ptz_') and name!='ptz_adapter':o.hide_render=True
render('02_open_rear',(.22,.3,.18),(.02,.01,.02),.20)
for name,o in objects.items():
    if name.startswith('user_pump'):o.hide_render=True
for name in ('front_bridge','rear_bridge'):objects[name].location.z+=.035
objects['gun_deck'].location.z+=.012
render('03_carrier_exploded',(.22,-.3,.24),(.02,.01,.035),.21)
