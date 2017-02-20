import PublishTemplate

#add to the left tool bar
mix = nuke.menu('Nodes').addMenu('Mix', icon = 'image.png')
mix.addCommand('PublishTemplate', 'PublishTemplate.main()', icon = 'image1.png')

#add to main menu
menuBar = nuke.menu('Nuke')
menuBar.addCommand('Edit/PublishTemplate','PublishTemplate.main()', icon = 'image2.png')

#add to the right click menu of node graph
nuke.menu('Node Graph').addCommand('PublishTemplate','PublishTemplate.main()')