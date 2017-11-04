import arcpy
import os
from arcpy import env

env.workspace = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"
arcpy.ListFeatureClasses()
for x in sorted(ListFeatureClasses):
    print (x)

# featureClassesForDeletion = ["LeftOver", "facCapture", "BufferUnion", "AlpineBuffer", "sumStats", "Buffer"]
featureClassesForDeletion = [C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossibleFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1_UnionFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_UnionFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_UnionF]
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossibleFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_Union
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer1_UnionFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_UnionFacCapture
C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb\sandyPossible_Buffer2_UnionF
]   
for featureClass in featureClassesForDeletion:
    arcpy.management.Delete(featureClass, None)

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)



# arcpy.env.overwriteOutput = True
# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
# arcpy.analysis.Buffer("Geocoding_Result_2_CopyFeatu2", r"C:\Users\Kyle\Dropbox\SS GIS-Zoning-Competition\Projects\SLCo\SLCo.gdb\GeoBuffer", "1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")


import arcpy
import os

env.workspace = r"C:\Users\Kyle\Desktop\Alpine AntiMatter Test\New Alpine AntiMatter Test.gdb"

datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        print(path)


