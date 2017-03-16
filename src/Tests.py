import nuke

files = ["C:\Users\priyansh shama\Documents\Nuke\Template\envir.nk",
        "C:\Users\priyansh shama\Documents\Nuke\Template\char.nk",
        "C:\Users\priyansh shama\Documents\Nuke\Template\crowd.nk"]

def buildCompScript():
    templates = files

    for i, template in enumerate(templates):
        nuke.scriptReadFile(template)
        nuke.selectAll()
        node = nuke.selectedNodes("BackdropNode")[0]

        if i > 0:
            bdNodes = node.getNodes()
            nodePrevX = node.xpos()
            nodePrevY = node.ypos()
            node.setYpos(previousNode.ypos() + 500)
            node.setXpos(previousNode.xpos())

            for n in bdNodes:
                if n.ypos() > nodePrevY:
                    n.setYpos(node.ypos()+(n.ypos()-nodePrevY))
                else:
                    n.setYpos(node.ypos()+(n.ypos()+nodePrevY))
                if n.xpos() > nodePrevX:
                    n.setXpos(node.xpos()+(n.xpos()-nodePrevX))
                else:
                    n.setXpos(node.xpos()+(n.xpos()+nodePrevX))
        
        previousNode = node

buildCompScript()
