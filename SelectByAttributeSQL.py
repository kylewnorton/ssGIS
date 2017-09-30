import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

arcpy.management.SelectLayerByAttribute("Zoning", "NEW_SELECTION", "ZONING = 'M2' Or ZONING = 'M1' Or ZONING = 'CG' Or ZONING = 'CS' Or ZONING = 'CBP' Or ZONING = 'CSD-11400 LPP' Or ZONING = 'CSD-LP' Or ZONING = 'CSD-WMBD'", None)
