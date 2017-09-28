# to select by attribute and then copy that to a new feature classs
import arcpy
arcpy.management.SelectLayerByAttribute("ACS_2015_5YR_BG_49_UTAH", "ADD_TO_SELECTION", "COUNTYFP = '049'", None)
arcpy.management.CopyFeatures("ACS_2015_5YR_BG_49_UTAH", r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Utah County\Novell Campus Storage\Novell Campus Storage.gdb\ACS_2015_5YR_BG_49_UTAH_Copy", None, None, None, None)
