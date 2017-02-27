import fnmatch
import os
from itertools import chain

def getTemplates():

    templateFiles = []
    paths = ('C:\Users\priyansh shama\Documents\Nuke\SHOW',
             'C:\Users\priyansh shama\Documents\Nuke\SEQUENCE',
             'C:\Users\priyansh shama\Documents\Nuke\SHOT')

    for path, dirnames, filenames in chain.from_iterable(os.walk(path) for path in paths):
        for filename in fnmatch.filter(filenames, '*.nk'):
            templateFiles.append(os.path.join(path, filename))

    templateDict = {}
    templateNames = []
    for file in templateFiles:
        filename = file.split("\\")[-1][:-3]
        locationType = os.path.dirname(file).split("\\")[-2]
        templateType = os.path.dirname(file).split("\\")[-1]
        templateName = locationType + ":" + templateType + ":" + filename
        templateNames.append(templateName)
        templateDict[templateName] = file

    #nuke.pluginPath()
    #nuke.menu("Nuke").addCommand("Custom/Test",nuke.message("Hello"))

    #print templateNames
    #print templateDict.keys()

    return templateNames, templateDict
