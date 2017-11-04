fields = ["renterPop", "supplyRatio"]
SumTables = ["SumStats3", "SumStats2", "SumStats1"]

for SumTable in SumTables:
        inFeatures = SumTable
        for field in fields
            fieldPrecision = 15
            arcpy.AddField_management(inFeatures, fieldNameIndex, "DOUBLE", fieldPrecision)



# instead...
# add fields to the feature class (or parcel)....totalPop3M, totalPop2M, totalPop1M,
# sum (of competition gross sq footage) in 3M, 2M, 1M; RenterPop3M, RenterPop2M, RenterPop1M,
# RenterPopPerc3M, renterPopPerc2M, renterPopPerc1M,  
