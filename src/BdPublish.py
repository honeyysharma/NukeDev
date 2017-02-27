import nuke
import os

def publishTemplate(outputPath, locationType, templateType, templateName, counter):
    # change directory to output path
    os.chdir(outputPath)
    # print os.getcwd()

    ## Check if the location folder already exists or not.
    if not os.path.exists(locationType):
        os.mkdir(locationType)

    # change directory path to the locationType
    os.chdir(outputPath + "/" + locationType)

    ## Check if the template folder already exists or not.
    if not os.path.exists(templateType):
        os.mkdir(templateType)

    newTemplatePath = outputPath + "/" + locationType + "/" + templateType + "/" + templateName + ".nk"
    # print newTemplatePath

    selectedNodes = nuke.selectedNodes()
    if counter == 1:
        selectedNodes = selectedNodes[::-1]

    # print [node.name() for node in oldSelectedNodes]
    if selectedNodes:
        print [node.name() for node in selectedNodes]
        viewerNodes = filter(lambda viewer: viewer.Class() == "Viewer", selectedNodes)
        if viewerNodes:
            selectedNodes = filter(lambda viewer: not viewer.Class() == "Viewer", selectedNodes)
            nukescripts.clear_selection_recursive()
            map(lambda node: node['selected'].setValue('True'), selectedNodes)
        if not selectedNodes[-1].Class() == "BackdropNode":
            newBd = nukescripts.autoBackdrop()
            newBd['selected'].setValue('True')
            selectedNodes.append(newBd)
            print [node.name() for node in selectedNodes]

        # check if file already exists
        if os.path.isfile(newTemplatePath):
            userInput = nuke.ask("The template already exists. Are you sure you want to override?")
            if userInput:
                nuke.nodeCopy(newTemplatePath)
            else:
                showPublishPanel(1)
        else:
            print newTemplatePath
            nuke.nodeCopy(newTemplatePath)
    else:
        nuke.message("Please select nodes!")


def showPublishPanel(counter):
    # Add GUI elements
    panel = nuke.Panel("Publish Template", 450)

    outputPath = ("/").join(nuke.Root().name().split('/')[0:-1])

    panel.setTitle("Publish Template to " + outputPath)
    panel.addSingleLineInput("Template Name:", "custom")
    panel.addEnumerationPulldown("Location:", "SHOT SEQUENCE SHOW")
    panel.addEnumerationPulldown("Template Type:", "ENVIR CHAR CROWD CUSTOM")
    panel.addButton("Cancel")
    panel.addButton("Publish Template")

    # Show GUI
    result = panel.show()

    # Check user selected template location
    if result == 1:
        templateName = panel.value("Template Name:")
        locationType = panel.value("Location:")
        templateType = panel.value("Template Type:")

        publishTemplate(outputPath, locationType, templateType, templateName, counter)


showPublishPanel(0)
