import bpy

from bpy.props import PointerProperty, FloatProperty
from bpy.types import PropertyGroup, Operator

from . import subdivide_fcurve

def get_selected_fcurves(context):
    selected_fcurve = []

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

class GraphEditorGetKeyframesOperator(Operator):
    '''gets current selected keyframes and prints them into the console'''

    bl_idname = "wm.graph_editor_get_keyframes"
    bl_label = "Get Keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    my_float_y : bpy.props.FloatProperty()

    @classmethod
    def poll(cls, context):
        areas = ('DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'TIMELINE')

        objects = context.selected_objects

        if context.area.type in areas:
            return True
        else:
            return False 


    def execute(self, context):
        selected_fcurves = get_selected_fcurves(context)

        for fcurve in selected_fcurves:
            selected_keyframes = get_selected_keyframes(fcurve)

            for keyframe in selected_keyframes:

                # https://docs.blender.org/api/current/bpy.types.Keyframe.html
                print("Keyframe", keyframe.type, keyframe.co)
                print("Left Handle", keyframe.handle_left_type, keyframe.handle_left)
                print("Right Handle", keyframe.handle_right_type, keyframe.handle_right)
                print("---")

            fcurve.update()
            
        return {'FINISHED'}

class GraphEditorDeleteKeyframesOperator(Operator):
    '''gets current selected keyframes and prints them into the console'''

    bl_idname = "wm.graph_editor_delete_keyframes"
    bl_label = "Delete Keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        areas = ('DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'TIMELINE')

        objects = context.selected_objects

        if context.area.type in areas:
            return True
        else:
            return False 


    def execute(self, context):
        selected_fcurves = get_selected_fcurves(context)
        
        for fcurve in selected_fcurves:
            selected_keyframes = get_selected_keyframes(fcurve)

            for keyframe in selected_keyframes:
                fcurve.keyframe_points.remove(keyframe)

            fcurve.update()

        return {'FINISHED'}

class GraphEditorInsertKeyframesOperator(Operator):
    '''gets current selected keyframes and prints them into the console'''

    bl_idname = "wm.graph_editor_insert_keyframes"
    bl_label = "Insert Keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        areas = ('DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'TIMELINE')

        objects = context.selected_objects

        if context.area.type in areas:
            return True
        else:
            return False 


    def execute(self, context):
        selected_fcurves = get_selected_fcurves(context)

        frame_current = context.scene.frame_current

        for selected_fcurve in selected_fcurves:

            subdivide_fcurve.subdivide_fcurve(selected_fcurve, frame_current)
            
        return {'FINISHED'}

classes = (
    GraphEditorGetKeyframesOperator,
    GraphEditorDeleteKeyframesOperator,
    GraphEditorInsertKeyframesOperator,
)
