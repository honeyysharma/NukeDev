import Experiments

templates = Experiments.getTemplates()[0]
templateDict = Experiments.getTemplates()[1]

nukeMenu = nuke.menu('Nuke')
miaTemplatesMenu = nukeMenu.addMenu("MIA Templates")

for template in templates:
    miaTemplatesMenu.addCommand(template,lambda template=template: nuke.scriptReadFile(templateDict[template]))
