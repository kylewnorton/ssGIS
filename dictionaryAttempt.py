# from time import strftime

# print ("Start script: + strftime("%Y-%m-%d %H:%M:%S")"")

import arcpy

sourceFC = "SL Co Competition Look up Table"

sourceFieldsList = ["City", "Zoning", "Allowed"]

# Use list comprehension to build a dictionary from a da SearchCursor where the key values are based on 3 separate feilds
valueDict = {str(r[0]) + "," + str(r[1]):(r[2:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFC = "SaltLakeZoning"

updateFieldsList = ["City", "ZONING", "Allowed"]

with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value by combining 3 field values of the row being updated in a keyValue variable
        keyValue = updateRow[0]+ "," + str(updateRow[1]) + "," + str(updateRow[2]
        # verify that the keyValue is in the Dictionary
        # if keyValue in valueDict:
            # transfer the value stored under the keyValue from the dictionary to the updated field.
            updateRow[2] = valueDict[keyValue][0]
            updateRows.updateRow(updateRow)

del valueDict

# print "Finished script: +strftime("%Y-%m-%d %H:%M:%S")"




# something I haven't used because I am trying the code above
import arcpy

ZoningDictionary = {}

MyCursor = arcpy.SearchCursor("SL Co Competition Look up Table")
for Feature in MyCursor:
    ZoningDictionary[Feature.getValue("City")] = Feature.getValue("Zoning")
del Feature
del MyCursor

LookupCursor = arcpy.UpdateCursor("SL Co Competition Look up Table")
for Feature in LookupCursor:
    Feature.setValue("NewPrice",ZoningDictionary[Feature.getValue("LookupField")])
del Feature
del LookupCursor


