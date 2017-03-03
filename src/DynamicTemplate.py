import nuke
import fileinput
import sys
import shutil
import os

def importTemplate(templateName, templateType):

    #set the script name according to template type
    if templateType == "ENVIR":
        filePath = "C:\Users\priyansh shama\Documents\Nuke\Template\envir.nk"
        tempFilePath = filePath.replace("envir.nk", "envir_temp.nk")
    elif templateType == "CHAR":
        filePath = "C:\Users\priyansh shama\Documents\Nuke\Template\char.nk"
        tempFilePath = filePath.replace("char.nk", "char_temp.nk")
    else:
        filePath = "C:\Users\priyansh shama\Documents\Nuke\Template\crowd.nk"
        tempFilePath = filePath.replace("crowd.nk", "crowd_temp.nk")


    #copy the template file to a temp file
    shutil.copy(filePath, tempFilePath)

    #open the script in the give path to replace the node name with template type
    # TEMPLATE_Read to ENVIR_Read
    for line in fileinput.input(tempFilePath, inplace=1):
        sys.stdout.write(line.replace("TEMPLATE", templateName))

    #import script
    nuke.scriptReadFile(tempFilePath)

    #remove temp file
    os.remove(tempFilePath)

# GUI code
def showTemplatePanel(templateType):

    # Add GUI elements
    panel = nuke.Panel("Publish Template", 350)

    panel.addSingleLineInput("Template Name:", templateType)
    panel.addButton("Cancel")
    panel.addButton("Import")

    # Show GUI
    result = panel.show()

    #if user publishes the template
    if result == 1:
        templateName = panel.value("Template Name:")
        importTemplate(templateName, templateType)
