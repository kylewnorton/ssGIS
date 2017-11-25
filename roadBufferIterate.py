import arcpy
import os
from arcpy import env
env.workspace = r"C:\Users\Kyle\Desktop\SS GIS-Zoning-Competition\SS GIS-Zoning-Competition\Projects\dynamicIterate2\dynamicIterate2.gdb"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.env.overwriteOutput = True

# VARIABLES
roads = "SLCoODOTRoadsFew"
roadBufferName = roads + "Buffer"
AADTFields = ["OBJECTID", "AADT2015"]
fieldToAddToRoads = "bufferSize"
updateField = ["OBJECTID", "bufferSize"]
#roadBuffer = {}
# VARIABLES

#arcpy.management.AddField(roads, fieldToAddToRoads, "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)	


#To populate the dictionary with the AADT values (using the original Object ID)
roadDict = {r[0]:int(r[1]) for r in arcpy.da.SearchCursor(roads, AADTFields)}
print (roadDict)

for key, value in roadDict.items():
    #print (key, 'corresponds to', roadDict[key])
	if value >= 65000:
		roadBufferDistance = 200
	elif 35000 <= value < 65000:
		roadBufferDistance = 100
	elif 15000 <= value < 35000:
		roadBufferDistance = 50
	else:
		roadBufferDistance = 30
	roadDict[key] = roadBufferDistance
print (roadDict)

#write values from the dictionary to the table for processing


with arcpy.da.UpdateCursor(roads, updateField) as updateRows:  
    for updateRow in updateRows:  
        # store the Join value of the row being updated in a keyValue variable  
        keyValue = updateRow[0]  
         # verify that the keyValue is in the Dictionary  
        if keyValue in roadDict:  
             # transfer the value stored under the keyValue from the dictionary to the updated field.  
            updateRow[1] = roadDict[keyValue]  
            updateRows.updateRow(updateRow)  


#with arcpy.da.UpdateCursor(roads, fieldToAddToRoads) as cursor:
#	for row in cursor:
#		row[0] =  
#		# Update the cursor with the updated list
#	cursor.updateRow(row)
		
			
#	roadBuffer [rowRoadBuffer[1]] = roadBufferDistance


#print (roadBuffer)


	#with arcpy.da.UpdateCursor(roads, fieldToAddToRoads) as cursor:
	#	for row in cursor:
	#		row[0] = roadBufferDistance  
	#		# Update the cursor with the updated list
	#	#cursor.updateRow(row)
arcpy.analysis.Buffer(roads, roadBufferName, "bufferSize", "FULL", "FLAT", "ALL", None, "PLANAR")

arcpy.Buffer_analysis(roads, roadBufferName, str(roadBufferDistance) + " Meters")



    #performLoop()

    #return;

#with arcpy.da.SearchCursor(roads, AADTFields) as cursorRoadBuffer:
#    for rowRoadBuffer in cursorRoadBuffer:
#        if float(rowRoadBuffer[1]) >= 65000:
#            roadBufferDistance = 200
#        elif 35000 <= float(rowRoadBuffer[1]) < 65000:
#            roadBufferDistance = 100
#        elif 15000 <= float(rowRoadBuffer[1]) < 35000:
#            roadBufferDistance = 50
#        else:
#            roadBufferDistance = 30


################################Don't Need this I believe#####################################

## VARIABLES
#censusOriginal = "SLCoTracts"
#tracts = "SLCoTractsSplitable0"
#filteredTractsOrig = "SLCoAntiMatterTracts"
#filteredTractsSplitable = "SLCoAntiMatterTractsSplitable"
#competition = "SLCoCompetition_GeocodeAddre"
#MetroPerCapitaSFMultiplier = 7.93
#radiusList = ["3", "2", "1"]
#inTableParcels = "SandySSParcelsFew"
#parcelField = "OBJECTID_1"
## VARIABLES


# i = 1

#with arcpy.da.SearchCursor(inTableParcels, parcelField) as cursor:
#    for row in cursor:
#        #PARCEL LOOP VARIABLES
#        roads = "road" + str(i)
#        inFeatures = [parcel, tracts]
#        filteredInFeatures = [parcel, filteredTractsSplitable]
#        parcelFeatureClassesForDeletion = [parcel]
#        #PARCEL LOOP VARIABLES

#        arcpy.management.MakeFeatureLayer(inTableParcels, parcel, "OBJECTID_1 = " + str(row[0]))


################################Don't Need this I believe#####################################