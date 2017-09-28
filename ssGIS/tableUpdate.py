# to update a table with city values
import arcpy
# Set local variables
in_table = "Sum_Stats"
field_names = "SFDemanded"
fieldPrecision = 15
fieldName2 = "NetSF"
fieldName3 = "NetSF95Occ"
fieldName4 = "FacilityID"

arcpy.da.UpdateCursor(in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause})


import arcpy

fc = "Zoning.SaltLakeZoning"
fields = ['City']

# Create update cursor for feature class
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    # Update the field used in Buffer so the distance is based on road
    # type. Road type is either 1, 2, 3, or 4. Distance is in meters.
    for row in cursor:
        # Update the BUFFER_DISTANCE field to be 100 times the
        # ROAD_TYPE field.
        row[1] = ("Salt Lake City")
        cursor.updateRow(row)
