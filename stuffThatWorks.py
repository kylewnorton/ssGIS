fc = "AlpineBufferUnionInside_Stat"
fieldList = arcpy.ListFields(fc)
for fields in fieldList:
    print (fields.name)

#Print the features and their populations that are within the buffer
fc = "AlpineBufferUnion"
fields = ["OBJECTID", "why_csv_Total_population"]
expression = "FID_AlpineBuffer = 1"
with arcpy.da.SearchCursor(fc, fields, expression) as cursor:
    for row in cursor:
        print('Feature {0} has a Total Population of {1}'.format(row[0], row[1]))
