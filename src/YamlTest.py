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
    for template in getTemplateList():
        print template

    #get nuke script to build
    #nuke.scriptOpen(inScript)

    #arrange templates in the given nuke script in vertical order
    """
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

    #save nuke script
    #nuke.scriptSave(outScript)

    #remove temp files

def buildCompScript():
    templates = getTemplateList()
    width = node.screenWidth()
    height = node.screenHeight()
    xpos = node.xpos()
    ypos = node.ypos()

    for template in templates:
        nuke.scriptReadFile(template)
        nuke.selectAll()
        node = nuke.selectedNodes("BackdropNode")[0]
        nodeNew.setXpos(xpos)
        nodeNew.setYpos(ypos + height + 50)
        height = nodeNew.screenHeight()
        xpos = nodeNew.xpos()
        ypos = nodeNew.ypos()

        width = node.screenWidth()
        height = node.screenHeight()
        xpos = node.xpos()
        ypos = node.ypos()

        # get nuke script to build
        # nuke.scriptOpen(inScript)

        # arrange templates in the given nuke script in vertical order

        # save nuke script
        # nuke.scriptSave(outScript)

        # remove temp files

buildCompScript()
