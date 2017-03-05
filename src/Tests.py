node = nuke.toNode("BackdropNode1")
print node.height(), node.width()
print node.screenHeight(), node.screenWidth()

width = node.screenWidth()
height = node.screenHeight()
ypos = node.ypos()
xpos = node.xpos()

for i in range(1,4):
    nodeNew = nuke.createNode("BackdropNode")
    nodeNew.setXpos(xpos)
    nodeNew.setYpos(ypos+height+50)
    height = nodeNew.screenHeight()
    xpos = nodeNew.xpos()
    ypos = nodeNew.ypos()
