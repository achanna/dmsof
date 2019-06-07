# Visit 2.12.2 log file
ScriptVersion = "2.12.2"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
visit.ShowAllWindows()
visit.OpenDatabase("solution.visit", 0)
# The UpdateDBPluginInfo RPC is not supported in the VisIt module so it will not be logged.
visit.AddPlot("Pseudocolor", "pressure", 1, 1)
visit.DrawPlots()
