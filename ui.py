
import bpy
from bpy.types import Panel, Menu

class CustomEditorPanel(Panel):
    bl_idname = 'CustomEditorPanel'
    bl_label = "Sliders"
    bl_region_type = 'UI'
    bl_category = 'Custom Editor'
    bl_space_type = 'GRAPH_EDITOR'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.graph_editor_get")

classes = (
    CustomEditorPanel,
)