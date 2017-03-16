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
    
"""
import nuke

templates = ["/homes/sharmah/nuke/temp1.nk", "/homes/sharmah/nuke/temp2.nk"]

nuke.scriptReadFile(templates[0])



bd1 = nuke.toNode("BackdropNode1")
print bd1.ypos()

bd2 = nuke.toNode("BackdropNode2")
print bd2.ypos()


bdNodes = bd2.getNodes()
bd2PrevX = bd2.xpos()
bd2PrevY = bd2.ypos()

bd2.setYpos(bd1.ypos() + 500)
bd2.setXpos(bd1.xpos())


print "Bd nodes"
for n in bdNodes:
    print n.name(),n.ypos()
    if n.ypos() > bd2PrevY:
        n.setYpos(bd2.ypos()+(n.ypos()-bd2PrevY))
    else:
        n.setYpos(bd2.ypos()+(n.ypos()+bd2PrevY))

    if n.xpos() > bd2PrevX:
        n.setXpos(bd2.xpos()+(n.xpos()-bd2PrevX))
    else:
        n.setXpos(bd2.xpos()+(n.xpos()+bd2PrevX))

"""
