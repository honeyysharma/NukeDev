import yaml
#import nuke
import fileinput
import sys

import shutil
import os

def importTemplate(templateName, templateType):

    #set the script name according to template type
    if templateType == "ENVIR":
        file = "C:\Users\priyansh shama\Documents\Nuke\Template\envir.nk"
        tempFile = file.replace("envir.nk", "temp_envir_"+templateName+".nk")
    elif templateType == "CHAR":
        file = "C:\Users\priyansh shama\Documents\Nuke\Template\char.nk"
        tempFile = file.replace("char.nk", "temp_char_"+templateName+".nk")
    else:
        file = "C:\Users\priyansh shama\Documents\Nuke\Template\crowd.nk"
        tempFile = file.replace("crowd.nk", "temp_crowd_"+templateName+".nk")


    #copy the template file to a temp file
    shutil.copy(file, tempFile)

    #open the script in the give path to replace the node name with template type
    # TEMPLATE_Read to ENVIR_Read
    for line in fileinput.input(tempFile, inplace=1):
        sys.stdout.write(line.replace("TEMPLATE", templateName))

    #return temp file
    return tempFile

def getTemplateList():
    templateDict = yaml.load("""
    Envir:
    - ENVIR
    - ENVIR_FG
    Char:
    - TIMMY
    - Boss
    Crowd:
    - CROWD_01
    - CROWD_02
    """)

    print templateDict

    envirList = templateDict['Envir']
    print envirList

    charList = templateDict['Char']
    print charList

    crowdList = templateDict['Crowd']
    print crowdList

    templateList = []
    for templateName in envirList:
        template = importTemplate(templateName, "ENVIR")
        templateList.append(template)

    for templateName in charList:
        template = importTemplate(templateName, "CHAR")
        templateList.append(template)

    for templateName in crowdList:
        template = importTemplate(templateName, "CROWD")
        templateList.append(template)

    return templateList

def buildCompScript():
    # get nuke script to build
    # nuke.scriptOpen(inScript)

    # arrange templates in the given nuke script in vertical order
    templates = getTemplateList()

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
                    n.setYpos(node.ypos() + (n.ypos() - nodePrevY))
                else:
                    n.setYpos(node.ypos() + (n.ypos() + nodePrevY))
                if n.xpos() > nodePrevX:
                    n.setXpos(node.xpos() + (n.xpos() - nodePrevX))
                else:
                    n.setXpos(node.xpos() + (n.xpos() + nodePrevX))

        previousNode = node

    #save nuke script
    #nuke.scriptSave(outScript)

    #remove temp files

buildCompScript()
