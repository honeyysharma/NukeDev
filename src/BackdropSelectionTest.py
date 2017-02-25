import nuke

nodes = nuke.selectedNodes()
if nodes and nodes[-1].Class() == "BackdropNode":
    #print bdNode.Class()
    #nukescripts.clear_selection_recursive()
    bdNode = nodes[-1]
    bdNode.selectNodes()
    nodesInBd = nuke.selectedNodes()
    viewerNodes = [node for node in nodesInBd if node.Class() == "Viewer"]
    nodesInBd = [node for node in nodesInBd if not node.Class() == "Viewer"]
    nukescripts.clear_selection_recursive()
    [node['selected'].setValue('True') for node in nodesInBd]
    #map(lambda viewer: viewer['selected'].setValue('False'), viewerNodes)
    #[viewer['selected'].setValue('False') for viewer in viewerNodes]
    #print viewerNodes
    #print [node.name() for node in nodesInBd]
else:
    nuke.message("Please select valid nodes!")
