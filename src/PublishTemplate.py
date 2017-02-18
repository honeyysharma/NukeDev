"""
Created on Feburary 14, 2017

@author: hsharma
"""

import nuke
import os
import shutil

## GUI code
def showPublishTemplatePanel():

    # Add GUI elements
    panel = nuke.Panel("Publish Template", 450)

    currentScriptName = nuke.Root().name().split('/')[-1][0:-3]

    panel.addSingleLineInput("Script Name:", currentScriptName)
    panel.addFilenameSearch("Output Path:", "Select Output Path")
    panel.addEnumerationPulldown("Select Nodes:", "All Selected")
    panel.addButton("Cancel")
    panel.addButton("Publish Template")

    # Show GUI
    result = panel.show()

    #if user publishes the template
    if result == 1:

        outputPath = panel.value("Output Path:")
        scriptName = panel.value("Script Name:")
        outputNodes = panel.value("Select Nodes:")

        ##Check for output path errors
        if outputPath == "Select Output Path":
            nuke.message("Please select output path")
            showPublishTemplatePanel()

        #Check if user input is all or selected nodes
        if outputNodes == "All": # ALL NODES IN THE CURRENT SCRIPT
            #pick all read nodes
            nodes = nuke.allNodes("Read")

            #select all the nodes
            nuke.selectAll()

            #copy selected nodes to a new nuke script
            nuke.nodeCopy(outputPath + scriptName + '.nk')
            return outputPath, scriptName, nodes
        else:
            ## Check if user has selected nodes
            if nuke.selectedNodes() == []:
                nuke.message("Please select the nodes.")
                #Don't bring up the tool
                return

            nodes = nuke.selectedNodes("Read") # SELECTED NODES IN THE CURRENT SCRIPT
            # copy selected nodes to a new nuke script
            nuke.nodeCopy(outputPath + scriptName + '.nk')

            return outputPath, scriptName, nodes


## Function to publish the template.
def publishTemplate(outputPath, scriptName, nodes):
    #print os.getcwd()
    os.chdir(outputPath)
    ## Check if the Sources folder already exists or not.
    if not os.path.exists('Sources'):
        os.mkdir('Sources')

    #new script
    newScriptName = outputPath + scriptName + '.nk'

    ##Iterate through given nodes
    for node in nodes:
        # Grab file path
        filePath = node.knob('file').getValue()

        #Split the file path
        splitPath = filePath.split('/')
        mediaPath = splitPath[-2] #media folder
        mediafile = splitPath[-1] #media file
        mediaExtension = mediafile[-4:]

        #complete path without the file
        sqFolder = filePath[:filePath.find(mediafile)]

        # If we have sequence of images
        if not mediafile.find('%') == -1:  #If not -1 or false this is a sq
            print 'This is a sq'
            #find padding
            padd = int(mediafile[mediafile.find('%')+2:mediafile.find('%')+3])

            #get the start and end of the sq
            firstFrame = int(node.knob('first').getValue())
            lastFrame = int(node.knob('last').getValue())

            #get sq name alone and with dot(.) at the end
            sqName = mediafile[:mediafile.find('%')-1]
            sqNameDot = mediafile[:mediafile.find('%')]

            #print sqName, sqNameDot, firstFrame, lastFrame

            #change to sources folder
            os.chdir(outputPath + 'Sources')

            #make dir to hold current sq
            if not os.path.exists(sqName):
                os.mkdir(sqName)

            #go into it
            os.chdir(sqName)

            #copy the files into sq folders by looping over frame range
            for frame in range(firstFrame, lastFrame+1):
                currentFile = sqFolder + sqNameDot + str(frame).zfill(padd) + mediaExtension

                copyFile = sqNameDot + str(frame).zfill(padd) + mediaExtension

                #copy the files
                shutil.copyfile(currentFile, copyFile)
        else:
            print 'This is not a sq'



def main():
    # show GUI
    data = showPublishTemplatePanel()

    #publish template at user selected path
    publishTemplate(data[0], data[1], data[2])

main()
