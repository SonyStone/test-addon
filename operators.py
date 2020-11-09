import bpy

from bpy.props import PointerProperty, FloatProperty
from bpy.types import PropertyGroup, Operator


def get_selected_keyframes(context):
    selected_keyframes = []
    for selected_visible_fcurve in context.selected_visible_fcurves:
        for keyframe in selected_visible_fcurve.keyframe_points:
            if keyframe.select_control_point:
                selected_keyframes.append(keyframe)

    return selected_keyframes

class GraphEditorGetOperator(Operator):
    '''gets current selected keyframes and prints them into the console'''

    bl_idname = "wm.graph_editor_get"
    bl_label = "Get Selected Keyframes"
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
        selected_keyframes = get_selected_keyframes(context)

        print("--- Selected Keyframes ---")
        for keyframe in selected_keyframes:

            # https://docs.blender.org/api/current/bpy.types.Keyframe.html
            print("Keyframe", keyframe.type, keyframe.co)
            print("Left Handle", keyframe.handle_left_type, keyframe.handle_left)
            print("Right Handle", keyframe.handle_right_type, keyframe.handle_right)
            print("---")
            
        return {'FINISHED'}

classes = (
    GraphEditorGetOperator,
)