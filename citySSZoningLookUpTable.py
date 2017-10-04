from time import strftime

print ("Start script: " + strftime("%Y-%m-%d %H:%M:%S"))

import arcpy
from arcpy import env
#
# # set the workspace so the path doesn't get so long and cause the buffer tool to not work
# env.workspace = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition"

sourceFC = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Salt Lake County\SLCoLookUpTable.csv"

sourceFieldsList = ["City", "Zoning", "Allowed"]

# Use list comprehension to build a dictionary from a da SearchCursor where the key values are based on 3 separate feilds
valueDict = {str(r[0]) + "," + str(r[1]):(r[2]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFC = r"\\Mac\Home\Desktop\SS GIS-Zoning-Competition\Utah\Salt Lake County\Salt Lake City\Zoning_Districts\Zoning_Districts.shp"

updateFieldsList = ["City", "ZONING", "Allowed"]

print (valueDict)

with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value by combining 3 field values of the row being updated in a keyValue variable
        keyValue = updateRow[0] + "," + str(updateRow[1])
        # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[2] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict
del updateRows

print ("Finished script: " +strftime("%Y-%m-%d %H:%M:%S"))
