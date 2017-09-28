# Prep environments
featureClassesForDeletion = ["LeftOver", "F1Capture", "BufferUnion", "Alpine_Buffer"]
for thingVariable in featureClassesForDeletion:
    arcpy.management.Delete(thingVariable, None)

fieldDeletion = ["NetSF", "NetSF95Occ"]
for field in fieldDeletion:
    arcpy.management.DeleteField("Alpine", field)
