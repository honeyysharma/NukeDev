import Experiments

templates = Experiments.getTemplates()[0]
templateDict = Experiments.getTemplates()[1]

def template():
    if templates:
        for template in templates:
            yield template

templateGen = template()

for i in range(0, len(templates)):
    #print "MIA Templates/" + template.next()
    #filename = templateDict[template.next()]
    templateName = templateGen.next()
    nuke.menu('Nuke').addCommand("MIA Templates/" + templateName, "nuke.message(templateDict[templateName])")
