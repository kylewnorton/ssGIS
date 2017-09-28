# Tool to get rid of items to start over when running a script
import arcpy
for featuretodelete in ["Sum_Stats1", "Sum_Stats2", "Sum_Stats3", "BufferUnion1", "BufferUnion2", "BufferUnion3", "F1Capture1", "F1Capture2", "F1Capture3", "LeftOver1", "LeftOver2", "LeftOver3"]:
    arcpy.management.Delete(featuretodelete, None)
