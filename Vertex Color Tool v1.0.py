from maya import cmds
import random

# Main function to create the custom UI window
def create_custom_window():
    # Check if the custom window already exists and delete it if true
    if cmds.window("customButtonWindow", exists=True):
        cmds.deleteUI("customButtonWindow")
        
    # Create a new window with menu bar and specific title and size
    cmds.window("customButtonWindow", menuBar=True, title="Vertex Color", widthHeight=(300, 250))
    cmds.columnLayout(adjustableColumn=True)
    cmds.menu(label='Help', helpMenu=True)

    # Add an "About" menu item that shows instructions when clicked
    cmds.menuItem(label="About", command=lambda *args: cmds.confirmDialog(
        title="About Vertex Color Tool",
        message=""" 
1. Apply Vertex Color
    - Select an Object: First, select the 3D object(s) you want to color.
    - Apply Vertex Color: Click the {apply_vertex_color} button. The tool will apply a random color to each vertex, using the {color_code_set} color set.

2. Remove All Color Sets
    - Select an Object: Select the object(s) with unwanted vertex color sets.
    - Remove Color Sets: Click the {remove_color_sets} button. This removes all color sets from the selected object(s) and resets vertex colors to default.

3. Switch to Texture or Vertex Color Sets
    - Select an Object: Choose the object(s) with multiple color sets.
    - Choose a Color Set:
        - Click {switch_to_texture} to activate the {color_texture_set} set.
        - Click {switch_to_vertex_color} to activate the {color_code_set} set.

4. Apply Random Color
    - Select an Object: Pick the object(s) to which you want to apply unique random vertex colors.
    - Apply Random Colors: Click {apply_random_color}. Each vertex will be assigned a random color, creating a unique look.

5. Apply Color Options
    - Open the Color Options Dialog: Click {apply_color_options}. This button opens Maya’s built-in Polygon Apply Color Options dialog, giving you control over advanced color options and settings.

Vertex Color Tool v1.0\nDeveloped by Kundan Basnet
""",
        button=["OK"]
    ))

    # Define each of the button functions for vertex color manipulation

    # Function to apply vertex color to selected objects
    def applyVertexColor():
        cmds.select(hi=True)  # Select all hierarchy objects
        selection = cmds.ls(selection=True)
        transforms = cmds.ls(sl=True, dag=True, type="mesh", long=True)  # Get only mesh objects
        cmds.select(transforms, r=True)
        selection = cmds.ls(sl=1)
        
        # Create two color sets for vertices
        cmds.polyColorSet(create=True, colorSet='colorTexture')
        cmds.polyColorSet(create=True, colorSet='colorCode')
        cmds.polyColorSet(currentColorSet=True, colorSet='colorCode')
        
        # Dictionary to group meshes by vertex count
        poly_dict = {}
        
        # Populate dictionary with meshes based on vertex count
        for mesh in selection:
            vert_count = cmds.polyEvaluate(mesh, vertex=1)
            if vert_count in poly_dict:
                poly_dict[vert_count].append(mesh)
            else:
                poly_dict[vert_count] = [mesh]
        
        # Apply random color to each vertex on all meshes grouped by vertex count
        for key, value in poly_dict.items():
            cmds.select(value)
            cmds.polyColorPerVertex(rgb=(random.uniform(0.0, .80), random.uniform(0.0, .80), random.uniform(0.0, .80)), colorDisplayOption=True)
            continue

    # Function to remove all color sets from selected objects
    def remove_colorSet():
        cmds.select(hi=True)
        selection = cmds.ls(selection=True)
        transforms = cmds.ls(sl=True, dag=True, type="mesh", long=True)
        cmds.select(transforms, r=True)
        colorSets = len(cmds.polyColorSet((selection), query=True, allColorSets=True))
        print(colorSets)
        
        # Loop to delete all color sets until none remain
        while colorSets > 0:
            cmds.polyColorSet(delete=True)
            print("All Color Set Cleared")

    # Function to switch the active color set to 'colorTexture'
    def colorTexture():
        cmds.select(hi=True)
        selection = cmds.ls(selection=True)
        transforms = cmds.ls(sl=True, dag=True, type="mesh", long=True)
        cmds.select(transforms, r=True)
        
        # Set 'colorTexture' as the current color set
        cmds.polyColorSet(currentColorSet=True, colorSet='colorTexture')
        cmds.select(clear=True)  # Clear selection

    # Function to switch the active color set to 'colorCode'
    def colorCode():
        cmds.select(hi=True)
        selection = cmds.ls(selection=True)
        transforms = cmds.ls(sl=True, dag=True, type="mesh", long=True)
        cmds.select(transforms, r=True)
        
        # Set 'colorCode' as the current color set
        cmds.polyColorSet(currentColorSet=True, colorSet='colorCode')
        cmds.select(clear=True)  # Clear selection

    # Function to apply random colors to each vertex in the 'colorCode' set
    def random_color():
        cmds.select(hi=True)
        selection = cmds.ls(selection=True)
        transforms = cmds.ls(sl=True, dag=True, type="mesh", long=True)
        
        # Set 'colorCode' as the current color set and apply random colors per vertex
        cmds.polyColorSet(currentColorSet=True, colorSet='colorCode')
        selected = cmds.ls(selection=True)
        if selected:
            for obj in selected:
                cmds.polyColorPerVertex(obj, rgb=(random.random(), random.random(), random.random()), colorDisplayOption=True)

    # Function to open Maya's built-in color options dialog
    def applyColor():
        import maya.mel as mm
        mm.eval("PolygonApplyColorOptions;")

    # Create buttons in the window, each linked to its function
    cmds.button(label="Apply Vertex Color", command=lambda x: applyVertexColor())
    cmds.button(label="Remove All Color Set", command=lambda x: remove_colorSet())
    cmds.button(label="Switch To Texture", command=lambda x: colorTexture())
    cmds.button(label="Switch To Vertex Color", command=lambda x: colorCode())
    cmds.button(label="Apply Random Color", command=lambda x: random_color())
    cmds.button(label="Apply Color Options", command=lambda x: applyColor())

    # Show the custom UI window
    cmds.showWindow("customButtonWindow")

# Call to create the custom window with all functionalities
create_custom_window()
