from time import strftime

print "Start script: " + strftime("%Y-%m-%d %H:%M:%S")

import arcpy

sourceFC = r"C:\Path\UpdateFeatureClass"

sourceFieldsList = ["UniqueValuesField", "NumberField"]

# Build a summary dictionary from a da SearchCursor with unique key values of a field storing a list of the sum of that value and the record count.
valueDict = {}
with arcpy.da.SearchCursor(sourceFC, sourceFieldsList) as searchRows:
    for searchRow in searchRows:
        keyValue = searchRow[0]
        if not keyValue in valueDict:
             # assign a new keyValue entry to the dictionary storing a list of the first NumberField value and 1 for the first record counter value
            valueDict[keyValue] = [searchRow[1], 1]
        # Sum the last summary of NumberField value with the current record and increment the record count when keyvalue is already in the dictionary
        else:
            valueDict[keyValue][0] += searchRow[1]
            valueDict[keyValue][1] += 1

updateFC = r"C:\Path\UpdateFeatureClass"

updateFieldsList = ["UniqueValuesField", "NumberField", "PercentField", "NumberSumField", "MeanField"]

with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as updateRows:
    for updateRow in updateRows:
        # store the Join value of the row being updated in a keyValue variable
        keyValue = updateRow[0]
        # verify that the keyValue is in the Dictionary
        if keyValue in valueDict:
            # divide the current record's NumberField value by the sum of the NumberField to get a percentage value
            updateRow[2] = updateRow[1] / valueDict[keyValue][0]
            # transfer the sum of the NumberField stored under the keyValue from the dictionary.
            updateRow[3] = valueDict[keyValue][0]
            # divide the sum of the NumberField value by the record count of the NumberField to get a mean value
            updateRow[4] = valueDict[keyValue][0] / valueDict[keyValue][1]
            updateRows.updateRow(updateRow)

del valueDict

print "Finished script: " + strftime("%Y-%m-%d %H:%M:%S")  
