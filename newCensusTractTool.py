import arcpy
from arcpy import env

# set the workspace so the path doesn't get so long and cause the buffer tool to not work
env.workspace = "C:/desktop/SS GIS-Zoning-Competition"

# to take care of weird projections
# Set the workspace, outputCoordinateSystem and maybe look at geographicTransformations environments if there are still problems
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

# VARIABLES
featureClassesForDeletion = ["LeftOverA1", "facCapture", "BufferUnion", "A1Buffer", "sumStats", "Buffer"]
fieldsForDeletion = ['OBJECTID', 'Shape', 'FID_AlpineBuffer', 'Loc_name', 'Status', 'Score', 'Match_type', 'Match_addr', 'LongLabel', 'ShortLabel', 'Addr_type', 'Type', 'PlaceName', 'Place_addr', 'Phone', 'URL', 'Rank', 'AddBldg', 'AddNum', 'AddNumFrom', 'AddNumTo', 'AddRange', 'Side', 'StPreDir', 'StPreType', 'StName', 'StType', 'StDir', 'BldgType', 'BldgName', 'LevelType', 'LevelName', 'UnitType', 'UnitName', 'SubAddr', 'StAddr', 'Block', 'Sector', 'Nbrhd', 'District', 'City', 'MetroArea', 'Subregion', 'Region', 'RegionAbbr', 'Territory', 'Zone', 'Postal', 'PostalExt', 'Country', 'LangCode', 'Distance', 'X', 'Y', 'DisplayX', 'DisplayY', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'ExInfo', 'IN_Address', 'IN_Address2', 'IN_Address3', 'IN_Neighborhood', 'IN_City', 'IN_Subregion', 'IN_Region', 'IN_Postal', 'IN_PostalExt', 'IN_CountryCode', 'USER_Object_ID', 'USER_Name_of_Store', 'USER_Street', 'USER_City', 'USER_St', 'USER_Zip', 'USER_Gross', 'USER_Net', 'USER_Notes', 'USER_Developer', 'USER_Status', 'USER_Units', 'USER_Date_Entered', 'USER_Groups', 'USER_10x10_climate', 'USER_10x10_non_climate', 'USER_Lattitude', 'USER_Longitude', 'USER_Field19', 'BUFF_DIST', 'ORIG_FID']
featureClass = "A1"
radius = .1
radiusIncrement = .4
supply = None
demand = None
netSquareFeet = None
facilityBufferName = featureClass + "Buffer"
censusTracts = "LeftOverFac2"
bufferUnion = "BufferUnion"
outPutInsideLayer = "facCapture"
outPutOutsideLayer = "LeftOverA1"
nameOfSumTable = "sumStats"
fieldToSum = "why_csv_Total_population" #is there a way to look this up?  Or should I have more code to get ready for this?
# could have python look up the table?
fieldNameToAdd = ["SFDemanded"]
popToSFMultiplier = 7.93
fieldToCalc = "SFDemanded"
# VARIABLES


# FUNCTIONS

# Reset environment


# FUNCTIONS


resetEnvironment(featureClassesForDeletion, fieldsForDeletion)

featureclass = "LeftOver"
fieldNames = [f.name for f in arcpy.ListFields(featureclass)]
print (fieldNames)

# copy the fields I want to Delete
fieldsForDeletion = ["OBJECTID", "Shape", "FID_AlpineBuffer", "Loc_name"]
for field in fieldsForDeletion:
    arcpy.management.DeleteField("LeftOver", field)

 , 'Status', 'Score', 'Match_type', 'Match_addr', 'LongLabel', 'ShortLabel', 'Addr_type', 'Type', 'PlaceName', 'Place_addr', 'Phone', 'URL', 'Rank', 'AddBldg', 'AddNum']'AddNumFrom', 'AddNumTo', 'AddRange', 'Side', 'StPreDir', 'StPreType', 'StName', 'StType', 'StDir', 'BldgType', 'BldgName', 'LevelType', 'LevelName', 'UnitType', 'UnitName', 'SubAddr', 'StAddr', 'Block', 'Sector', 'Nbrhd', 'District', 'City', 'MetroArea', 'Subregion', 'Region', 'RegionAbbr', 'Territory', 'Zone', 'Postal', 'PostalExt', 'Country', 'LangCode', 'Distance', 'X', 'Y', 'DisplayX', 'DisplayY', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'ExInfo', 'IN_Address', 'IN_Address2', 'IN_Address3', 'IN_Neighborhood', 'IN_City', 'IN_Subregion', 'IN_Region', 'IN_Postal', 'IN_PostalExt', 'IN_CountryCode', 'USER_Object_ID', 'USER_Name_of_Store', 'USER_Street', 'USER_City', 'USER_St', 'USER_Zip', 'USER_Gross', 'USER_Net', 'USER_Notes', 'USER_Developer', 'USER_Status', 'USER_Units', 'USER_Date_Entered', 'USER_Groups', 'USER_10x10_climate', 'USER_10x10_non_climate', 'USER_Lattitude', 'USER_Longitude', 'USER_Field19', 'BUFF_DIST', 'ORIG_FID']
