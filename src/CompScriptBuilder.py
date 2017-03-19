import yaml
import nuke
import fileinput
import sys
import argparse
import shutil
import os.path

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

def getTemplateList(layerOrderFile):

    #open layer order file and store the output into a dictionary
    with open(layerOrderFile, 'r') as stream:
        templateDict = yaml.load(stream)

    #static templates
    mpaintTemplate = "C:\Users\priyansh shama\Documents\Nuke\Template\mpaint.nk"
    outputTemplate = "C:\Users\priyansh shama\Documents\Nuke\Template\output.nk"

    #dynamic templates
    envirList = templateDict['Envir']
    charList = templateDict['Char']
    crowdList = templateDict['Crowd']

    #list to collect all the templates
    templateList = []

    templateList.append(mpaintTemplate)

    for templateName in envirList:
        template = importTemplate(templateName, "ENVIR")
        templateList.append(template)

    for templateName in charList:
        template = importTemplate(templateName, "CHAR")
        templateList.append(template)

    for templateName in crowdList:
        template = importTemplate(templateName, "CROWD")
        templateList.append(template)

    templateList.append(outputTemplate)

    return templateList

def buildCompScript(layerOrderFile, compScriptFile):
    # get nuke script to build
    nuke.scriptOpen(compScriptFile)

    # arrange templates in the given nuke script in vertical order
    templates = getTemplateList(layerOrderFile)

    for i, template in enumerate(templates):
        nuke.scriptReadFile(template)
        nuke.selectAll()
        node = nuke.selectedNodes("BackdropNode")[0]
        dotNode = nuke.selectedNodes('Dot')[0]
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

            if i > 1:
                dotNode.setInput(0, previousDotNode.dependent()[0])
            else:
                dotNode.setInput(0, previousDotNode)

        previousNode = node
        previousDotNode = dotNode

        # save nuke script
        nuke.scriptSave(compScriptFile)

        # remove temp files

def main():
    #should take a list of shots
    shotDir = "C:\Users\priyansh shama\Documents\Nuke"

    parser = argparse.ArgumentParser("This scripts builds your comp script.")

    #make it optional, should read from given shots' dir
    parser.add_argument('-i', '--input', help="Input Layer Order name", required = True)
    parser.add_argument('-c', '--comp', help="Optional input Comp Script name")
    args = parser.parse_args()

    layerOrderFile = shotDir + "\\" + args.input
    if os.path.isfile(layerOrderFile):
        print ("Input: %s" % layerOrderFile)
    else:
        print "The layer order file name is not valid"
        sys.exit()

    if args.comp is None:
        compScriptFile = shotDir + "\\" + "comp.nk"
    else:
        compScriptFile = args.comp
    if os.path.isfile(compScriptFile):
        print ("Comp: %s" % compScriptFile)
    else:
        print "Comp script doesn't exists."
        sys.exit()

    #buildCompScript(layerOrderFile, compScriptFile)

if __name__ == "__main__":
    main()

#Check if the given file paths exists or not

