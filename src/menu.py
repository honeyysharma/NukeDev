import DynamicTemplate
import Experiments

nuke.menu('Nodes').addCommand("Backdrop", "nukescripts.autoBackdrop()")

nukeMenu = nuke.menu('Nuke')
miaTemplatesMenu = nukeMenu.addMenu("MIA Templates")

miaTemplatesMenu.addCommand("Dynamic/Envir", 'DynamicTemplate.showTemplatePanel("ENVIR")')
miaTemplatesMenu.addCommand("Dynamic/Char", 'DynamicTemplate.showTemplatePanel("CHAR")')
miaTemplatesMenu.addCommand("Dynamic/Crowd", 'DynamicTemplate.showTemplatePanel("CROWD")')

templates = Experiments.getTemplates()[0]
templateDict = Experiments.getTemplates()[1]

if templates:
    for template in templates:
        miaTemplatesMenu.addCommand(template,lambda template=template: nuke.scriptReadFile(templateDict[template]))

"""
import PublishTemplate

#add to the left tool bar
mix = nuke.menu('Nodes').addMenu('Mix', icon = 'image.png')
mix.addCommand('PublishTemplate', 'PublishTemplate.main()', icon = 'image1.png')

#add to main menu
menuBar = nuke.menu('Nuke')
menuBar.addCommand('Edit/PublishTemplate','PublishTemplate.main()', icon = 'image2.png')

#add to the right click menu of node graph
nuke.menu('Node Graph').addCommand('PublishTemplate','PublishTemplate.main()')
"""
