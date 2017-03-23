import sys
import yaml
import fileinput
import argparse
import shutil
import os.path

def importTemplate(templateName, templateType):

    templateDir = "C:\Users\priyansh shama\Documents\Nuke\Template"
    #set the script name according to template type
    if templateType == "ENVIR":
        file = templateDir + "\envir.nk"
        tempFile = file.replace("envir.nk", "temp_envir_"+templateName+".nk")
    elif templateType == "CHAR":
        file = templateDir + "\char.nk"
        tempFile = file.replace("char.nk", "temp_char_"+templateName+".nk")
    else:
        file = templateDir + "\crowd.nk"
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

    #####Convert all the paths into macros#####

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

#Should only accept shot path, layer order filename and comp script filename
#and a flag to determine if script is running from the comp itself or command line.
#example C:\Users\priyansh shama\Documents\Nuke\sq100\s10, layer_order.yml, comp.nk, isRunningFromScript
def buildCompScript(layerOrderFile, compScriptFile):

    #imported nuke here as importing it outside was breaking argparse
    import nuke

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
    #should take a sequence and a list of shots
    prodDir = "C:\Users\priyansh shama\Documents\Nuke"

    parser = argparse.ArgumentParser("This scripts builds your comp script.")

    #make it optional, should read from given shots' dir
    parser.add_argument('-sq', '--sequence', type=int, help="The sequence for you want to build the script.", required=True)
    parser.add_argument('-s', '--shots', nargs='*', type=int, help="The shots for you want to build the script.")
    parser.add_argument('-i', '--input', help="Input Layer Order name")
    parser.add_argument('-c', '--comp', help="Optional input Comp Script name")
    args = parser.parse_args()

    #check if sequence dir exists or not
    if args.sequence is not None:
        sqDir = prodDir + "\\" + "sq" + str(args.sequence)
        print sqDir

    if args.shots is not None:
        shots = map(lambda x: "s"+str(x), args.shots)
        print shots
    else:
        #look for shot dirs in the sqDir, if nothing raise exception and exit
        pass

    for shot in shots:
        shotDir = sqDir + "\\" + shot
        print shotDir
        #check if path exists or not

    #can be moved to buildCompScript() or inside above loop of shots
    #corret path to prodDir + sqDir + shotDir + layer_order.yml
    if args.input is None:
        layerOrderFile = prodDir + "\\" + "layer_order.yml"
    else:
        layerOrderFile = args.input
    if os.path.isfile(layerOrderFile):
        print ("Input: %s" % layerOrderFile)
    else:
        print "The layer order file name is not valid"
        sys.exit()

    # corret path to prodDir + sqDir + shotDir + comp.nk
    if args.comp is None:
        compScriptFile = prodDir + "\\" + "comp.nk"
    else:
        compScriptFile = args.comp
    if os.path.isfile(compScriptFile):
        print ("Comp: %s" % compScriptFile)
    else:
        print "Comp script doesn't exists."
        sys.exit()

    print args.sequence
    print args.shots

    #buildCompScript(layerOrderFile, compScriptFile)

if __name__ == "__main__":
    main()

#Check if the given file paths exists or not
