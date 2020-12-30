import bpy

from bpy.props import PointerProperty, FloatProperty
from bpy.types import PropertyGroup, Operator

from . import subdivide_fcurve

def get_selected_fcurves(context):
    selected_fcurve = []

    # https://docs.blender.org/api/current/bpy.context.html#bpy.context.selected_visible_fcurves
    for selected_visible_fcurve in context.selected_visible_fcurves:
        if selected_visible_fcurve.select:
            selected_fcurve.append(selected_visible_fcurve)

    return selected_fcurve

def get_selected_keyframes(fcurve):

    selected_keyframes = []

    keyframes = []

    for keyframe in fcurve.keyframe_points:

        # selected_visible_fcurve.keyframe_points.insert(1, 6)
        keyframes.append(keyframe.select_control_point)

        if keyframe.select_control_point:
            selected_keyframes.append(keyframe)

            
    return selected_keyframes

def set_select_keyframe(keyframe, boolean):
    
    keyframe.select_control_point = boolean
    keyframe.select_left_handle = boolean
    keyframe.select_right_handle = boolean

class GraphEditorGetKeyframesOperator(Operator):
    '''gets current selected keyframes and prints them into the console'''

    bl_idname = "wm.graph_editor_get_keyframes"
    bl_label = "Process"
    bl_options = {'REGISTER', 'UNDO'}

    my_float_y : bpy.props.FloatProperty()

    @classmethod
    def poll(cls, context):
        areas = ('DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'TIMELINE')

        if context.area.type in areas:
            return True
        else:
            return False 

    def execute(self, context):
        '''
        [FCurve](https://docs.blender.org/api/current/bpy.types.FCurve.html)
        [Keyframe](https://docs.blender.org/api/current/bpy.types.Keyframe.html)
        [graph.delete](https://docs.blender.org/api/current/bpy.ops.graph.html#bpy.ops.graph.delete)
        [FCurveKeyframePoints](https://docs.blender.org/api/current/bpy.types.FCurveKeyframePoints.html)
        '''
        selected_fcurves = get_selected_fcurves(context)

        for fcurve in selected_fcurves:

            selected_keyframes = get_selected_keyframes(fcurve)

            for keyframe in reversed(selected_keyframes[1:]):
                fcurve.keyframe_points.remove(keyframe, fast=True)

            selected_keyframes[0].co.y = selected_keyframes[0].co.y # workaround for fcurve.update

            fcurve.update() # not updating view

            
        return {'FINISHED'}


classes = (
    GraphEditorGetKeyframesOperator,
)
