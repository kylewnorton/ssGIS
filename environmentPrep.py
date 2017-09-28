# Prep environments
featureClassesForDeletion = ["LeftOver", "F1Capture", "BufferUnion", "Alpine_Buffer"]
for thingVariable in featureClassesForDeletion:
    arcpy.management.Delete(thingVariable, None)

fieldDeletion = ["NetSF", "NetSF95Occ"]
for field in fieldDeletion:
    arcpy.management.DeleteField("Alpine", field)

# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
# arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
