#!/usr/bin/python
import xml.etree.ElementTree as ET
from shutil import copy
import sys
import os

def dump():
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    print str(len(entities)) + " Entities Loaded"
    for entity in entities:
        print ""
        print entity.find("Name").text
        forms = entity.findall("FormXml/forms")
        print str(len(forms)) + " Forms"
        for form in forms:
            print ""
            print form.get("type")
            events = form.findall("systemform/form/events/event")
            for event in events:
                print ""
                eventType = event.get("name") 
                if eventType == "onchange":
                    print "onchange: " + event.get("attribute")
                else:
                    print eventType
                handlers = event.findall("Handlers/Handler")
                for handler in handlers:
                    print "  " +handler.get("libraryName") + ":" + handler.get("functionName")

def dumpForEntity(entityName,formType):
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    for entity in entities:
        if entity.find("Name").text == entityName:
            forms = entity.findall("FormXml/forms")
            for form in forms:
                if form.get("type") == formType:
                    events = form.findall("systemform/form/events/event")
                    for event in events:
                        print ""
                        eventType = event.get("name") 
                        if eventType == "onchange":
                            print "onchange: " + event.get("attribute")
                        else:
                            print eventType
                        handlers = event.findall("Handlers/Handler")
                        for handler in handlers:
                            print "  " +handler.get("libraryName") + ":" + handler.get("functionName")

def dumpLibrariesForEntity(entityName,formType):
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    libraries = {}
    for entity in entities:
        if entity.find("Name").text == entityName:
            forms = entity.findall("FormXml/forms")
            for form in forms:
                if form.get("type") == formType:
                    events = form.findall("systemform/form/events/event")
                    for event in events:
                        eventType = event.get("name") 
                        handlers = event.findall("Handlers/Handler")
                        for handler in handlers:
                            if handler.get("libraryName") in libraries:
                                if not any(handler.get("functionName") in l for l in libraries[handler.get("libraryName")] ):
                                    libraries[handler.get("libraryName")].append(handler.get("functionName"))
                            else:
                                libraries[handler.get("libraryName")] = []
                                libraries[handler.get("libraryName")].append(handler.get("functionName"))
    for key in libraries:
        print ""
        print key + ":"
        for f in libraries[key]:
            print f

def copyWebResources():
    customizations = ET.parse("customizations.xml")
    resources = customizations.findall("./WebResources/WebResource")
    print len(resources)
    outdir = "output"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for r in resources:
        name = r.find("Name")
        path = r.find("FileName")
        if name != None and path != None:
            print name.text + " " + path.text
            if ("/" in name.text):
                os.makedirs(os.path.join(outdir, name.text))
            copy("." + path.text,os.path.join(outdir, name.text))
    
def listRibbonScripts(entityName):
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    ribbonLibraries = {}
    for entity in entities:
        if (entity.find("Name").text == entityName) or (entityName == "all"):
            ribbonScripts = entity.findall("./RibbonDiffXml/CommandDefinitions/CommandDefinition/Actions/JavaScriptFunction")
            for script in ribbonScripts:
                scriptName = script.get("Library")
                scriptFunction = script.get("FunctionName")
                if "$webresource:" in scriptName:
                    scriptName=scriptName.replace("$webresource:","")
                if scriptName in ribbonLibraries:
                    if not any(scriptFunction in l for l in ribbonLibraries[scriptName] ):
                        ribbonLibraries[scriptName].append(scriptFunction)
                else:
                    ribbonLibraries[scriptName] = []
                    ribbonLibraries[scriptName].append(scriptFunction)
    
    for key in ribbonLibraries:
        print ""
        print key + ":"
        for f in ribbonLibraries[key]:
            print f
                
def dumpEntityFields(entityName):
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    for entity in entities:
        if (entity.find("Name").text == entityName) or (entityName == "all"):
            if entityName == "all":
                print entity.find("Name").text
            attributes = entity.findall("./EntityInfo/entity/attributes/attribute")
            for attribute in attributes:
                print attribute.get("PhysicalName")
def dumpWorkflows():
    customizations = ET.parse("customizations.xml")
    workflows = customizations.findall("./Workflows/Workflow")
    for workflow in workflows:
        print workflow.get("Name")

def dumpEntities():
    customizations = ET.parse("customizations.xml")
    entities = customizations.findall("./Entities/Entity")
    for entity in entities:
            print entity.find("Name").text

def dumpReports():
    customizations = ET.parse("customizations.xml")
    reports = customizations.findall("./Reports/Report")
    for report in reports:
        print report.find("name").text

def main():
    if len(sys.argv)!=1:
        if sys.argv[1]=="handlers":
            if len(sys.argv) >=3:
                dumpForEntity(sys.argv[2],sys.argv[3])
            else:
                print "Not enough args"
        elif sys.argv[1] == "libraries":
            if len(sys.argv) >=3:
                dumpLibrariesForEntity(sys.argv[2],sys.argv[3])
            else:
                print "Not enough args"
        elif sys.argv[1] == "resources":
            copyWebResources()
        elif sys.argv[1] == "ribbon":
            if len(sys.argv) >=2:
                listRibbonScripts(sys.argv[2])
            else:
                print "Not enough args"
        elif sys.argv[1] == "fields":
            if len(sys.argv) >=2:
                dumpEntityFields(sys.argv[2])
            else:
                print "Not enough args"
        elif sys.argv[1] == "entities":
                dumpEntities()
        elif sys.argv[1] == "workflows":
                dumpWorkflows()
        elif sys.argv[1] == "reports":
                dumpReports()
            
    else:
        dump()

main()
