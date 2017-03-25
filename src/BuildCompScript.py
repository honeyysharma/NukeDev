import sys
import yaml
import fileinput
import argparse
import shutil
import os.path


# import nuke

def importTemplate(templateName, templateType):
    templateDir = os.path.abspath("C:\Users\priyansh shama\Documents\Nuke\Template")

    # set the script name according to template type
    if templateType == "ENVIR":
        file = os.path.join(templateDir, "envir.nk")
        tempFile = file.replace("envir.nk", "temp_" + templateName + "_" + templateType + ".nk")
    elif templateType == "CHAR":
        file = templateDir + "\char.nk"
        tempFile = file.replace("char.nk", "temp_" + templateName + "_" + templateType + ".nk")
    else:
        file = templateDir + "\crowd.nk"
        tempFile = file.replace("crowd.nk", "temp_" + templateName + "_" + templateType + ".nk")

    # copy the template file to a temp file
    shutil.copy(file, tempFile)

    # open the script in the give path to replace the node name with template type
    # TEMPLATE_Read to ENVIR_Read
    for line in fileinput.input(tempFile, inplace=1):
        sys.stdout.write(line.replace("TEMPLATE", templateName))

    # return temp file
    return tempFile


def getTemplateList(layerOrderFile):
    # open layer order file and store the output into a dictionary
    with open(layerOrderFile, 'r') as stream:
        templateDict = yaml.load(stream)

    # static templates
    mpaintTemplate = "C:\Users\priyansh shama\Documents\Nuke\Template\mpaint.nk"
    outputTemplate = "C:\Users\priyansh shama\Documents\Nuke\Template\output.nk"

    # list to collect all the templates
    templateList = []

    templateList.append(mpaintTemplate)

    # dynamic templates
    if "Envir" in templateDict.keys():
        envirList = templateDict['Envir']
        if envirList:
            for templateName in envirList:
                template = importTemplate(templateName, "ENVIR")
                templateList.append(template)

    if "Char" in templateDict.keys():
        charList = templateDict['Char']
        if charList:
            for templateName in charList:
                template = importTemplate(templateName, "CHAR")
                templateList.append(template)

    if "Crowd" in templateDict.keys():
        crowdList = templateDict['Crowd']
        if crowdList:
            for templateName in crowdList:
                template = importTemplate(templateName, "CROWD")
                templateList.append(template)

    templateList.append(outputTemplate)

    return templateList


# method to build comp script from the existing comp
def buildCompScriptFromCurrentScript():
    currentCompScript = nuke.root().name()
    currentDir = os.path.dirname(currentCompScript)

    fileList = [file for file in os.listdir(currentDir) if "layer_order.yml" in file]
    if fileList:
        layerOrderFile = os.path.join(currentDir, fileList[0])
        currentCompScript = os.path.join(currentCompScript, "comp.nk")
        buildCompScript(layerOrderFile, currentCompScript, True)
    else:
        nuke.message("Could not find layer-order.yml in the current comp directory!")


def buildCompScript(layerOrderFile, compScriptFile, isRunningFromScript):
    # kept here if script is run from the comp itself
    if not os.path.isfile(layerOrderFile):
        print "Could not find layer_order.yml in " + shotDir
        sys.exit()

    if not isRunningFromScript:
        nuke.scriptClear()
        # get nuke script to build
        nuke.scriptOpen(compScriptFile)
        nuke.selectAll()
        [nuke.delete(node) for node in nuke.selectedNodes()]

    # arrange templates in the given nuke script in vertical order
    templates = getTemplateList(layerOrderFile)

    for i, template in enumerate(templates):
        nuke.nodePaste(template)
        bdNodes = nuke.selectedNodes()
        node = nuke.selectedNodes("BackdropNode")[0]
        dotNode = nuke.selectedNodes('Dot')[0]

        if i > 0:
            bdNodes.remove(node)
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

    if not isRunningFromScript:
        # save nuke script
        nuke.scriptSave(compScriptFile)
        # avoid opening GUI and getting extra nodes from previous script
        nuke.scriptClose()

    # remove temp files
    [os.remove(template) for template in templates if "temp" in template]


def main():
    # should take a sequence and a list of shots
    prodDir = "C:\Users\priyansh shama\Documents\Nuke"

    parser = argparse.ArgumentParser("This scripts builds your comp script.")

    # make it optional, should read from given shots' dir
    parser.add_argument('-sq', '--sequence', help="Example: sq100 - The sequence for you want to build the script.",
                        required=True)
    parser.add_argument('-s', '--shots', nargs='*',
                        help="Example: s10 s20 - The shots for you want to build the script.")
    parser.add_argument('-i', '--input', help="Input Layer Order name")
    parser.add_argument('-c', '--comp', help="Optional input Comp Script name")
    args = parser.parse_args()

    # check if sequence dir exists or not
    if args.sequence is not None:
        sqDir = os.path.join(prodDir, str(args.sequence))

    if os.path.isdir(sqDir):
        if args.shots is None:
            # look for shot dirs in the sqDir, if nothing raise exception and exit
            shots = [name for name in os.listdir(sqDir) if "s" in name]
        else:
            shots = args.shots

        if not shots:
            print "No shot dir found!"
            sys.exit()
        else:
            for shot in shots:
                shotDir = os.path.join(sqDir, shot)
                # check if path exists or not
                if os.path.isdir(shotDir):
                    # correct path to prodDir + sqDir + shotDir + layer_order.yml
                    if args.input is None:
                        layerOrderFile = os.path.join(shotDir, "layer_order.yml")
                    else:
                        layerOrderFile = args.input

                    # correct path to prodDir + sqDir + shotDir + comp.nk
                    if args.comp is None:
                        compScriptFile = os.path.join(shotDir, "comp.nk")
                    else:
                        compScriptFile = args.comp

                    if not os.path.isfile(compScriptFile):
                        print "Could not find comp.nk in " + shotDir
                        sys.exit()

                    buildCompScript(layerOrderFile, compScriptFile, False)
                else:
                    print "The shot directory " + shot + " does not exists!"
                    sys.exit()
    else:
        print "The sequence directory " + "sq" + str(args.sequence) + " does not exists!"


if __name__ == "__main__":
    main()
