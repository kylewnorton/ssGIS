import arcpy
from arcpy import env

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")

arcpy.env.overwriteOutput = True

#To make feature "Divisible" or "Splitable"
arcpy.management.MakeFeatureLayer("SLCoTracts", "SLCoTractsSplitable", None, None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;tl_2016_49_tract_STATEFP tl_2016_49_tract_STATEFP VISIBLE NONE;tl_2016_49_tract_COUNTYFP tl_2016_49_tract_COUNTYFP VISIBLE NONE;tl_2016_49_tract_TRACTCE tl_2016_49_tract_TRACTCE VISIBLE NONE;tl_2016_49_tract_GEOID tl_2016_49_tract_GEOID VISIBLE NONE;tl_2016_49_tract_NAME tl_2016_49_tract_NAME VISIBLE NONE;tl_2016_49_tract_NAMELSAD tl_2016_49_tract_NAMELSAD VISIBLE NONE;tl_2016_49_tract_MTFCC tl_2016_49_tract_MTFCC VISIBLE NONE;tl_2016_49_tract_FUNCSTAT tl_2016_49_tract_FUNCSTAT VISIBLE NONE;tl_2016_49_tract_ALAND tl_2016_49_tract_ALAND VISIBLE NONE;tl_2016_49_tract_AWATER tl_2016_49_tract_AWATER VISIBLE NONE;tl_2016_49_tract_INTPTLAT tl_2016_49_tract_INTPTLAT VISIBLE NONE;tl_2016_49_tract_INTPTLON tl_2016_49_tract_INTPTLON VISIBLE NONE;tl_2016_49_tract_Id2 tl_2016_49_tract_Id2 VISIBLE NONE;why_csv_Id why_csv_Id VISIBLE NONE;why_csv_Id2 why_csv_Id2 VISIBLE NONE;why_csv_Geography why_csv_Geography VISIBLE NONE;why_csv_Total_population why_csv_Total_population VISIBLE RATIO;why_csv_Median_age_years why_csv_Median_age_years VISIBLE NONE;why_csv_TotalHouseholds why_csv_TotalHouseholds VISIBLE NONE;why_csv_AvgHouseholdSize why_csv_AvgHouseholdSize VISIBLE NONE;why_csv_TotalFamilies why_csv_TotalFamilies VISIBLE NONE;why_csv_Percent_Owner_occupied_housing_units why_csv_Percent_Owner_occupied_housing_units VISIBLE NONE;why_csv_Percent_Renter_occupied_housing_units why_csv_Percent_Renter_occupied_housing_units VISIBLE NONE;why_csv_Owner_Occupied_Housing_Units why_csv_Owner_Occupied_Housing_Units VISIBLE NONE;why_csv_Renter_Occupied_Housing_Units why_csv_Renter_Occupied_Housing_Units VISIBLE NONE;why_csv_average_Household_income why_csv_average_Household_income VISIBLE NONE;why_csv_Median_Household_income why_csv_Median_Household_income VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE RATIO;HundredPCT HundredPCT VISIBLE NONE;OrigTotPop OrigTotPop VISIBLE NONE")

#Buffer Creation
arcpy.analysis.Buffer("Alpine", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBuffer", "1 Miles", "FULL", "ROUND", "NONE", None, "PLANAR")

#union between buffer and census tracts (divisible)
#arcpy.analysis.Union("alpinebuffer #;slcotractssplitable #", r"c:\users\kyle\desktop\temp\uniondebug\uniondebug.gdb\alpinebufferunion", "all", none, "gaps")

arcpy.analysis.Union("AlpineBuffer #;SLCoTractsSplitable #", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnion", "ALL", None, "GAPS")


#selection of just the portion of the census tracts within the buffer
arcpy.management.SelectLayerByAttribute("AlpineBufferUnion", "NEW_SELECTION", "FID_AlpineBuffer = 1", None)

#creating a new feature class from the selection above
arcpy.management.CopyFeatures("AlpineBufferUnion", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnionInside", None, None, None, None)

#total of population from the selected portions of the census tracts
arcpy.analysis.Statistics("AlpineBufferUnionInside", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnionInside_Stat", "why_csv_Total_population SUM", None)

#print the total of population from the sumation of the census tracts populations from above
fc = "AlpineBufferUnionInside_Stat"
totPop = "Sum_why_csv_Total_population"
cursor = arcpy.SearchCursor(fc)
for rowdemand in cursor:
    totalPopulationInsideBuffer = (rowdemand.getValue(totPop))
print("Total Population from Split Policy Census Tracts:", totalPopulationInsideBuffer)






#This section is for the Non-Divisible Census Tracts to show the difference between Ratio'd and Not. 
#Union between Buffer and Census Tracts (Non-Divisible)
arcpy.analysis.Union("AlpineBuffer #;SLCoTracts #", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnionNonSplit", "ALL", None, "GAPS")

#Selection of just the portion of the Census Tracts within the Buffer
arcpy.management.SelectLayerByAttribute("AlpineBufferUnionNonSplit", "NEW_SELECTION", "FID_AlpineBuffer = 1", None)

#Creating a new feature class from the selection above
arcpy.management.CopyFeatures("AlpineBufferUnionNonSplit", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnionInsideNonSplit", None, None, None, None)

#Total of Population from the selected portions of the Census Tracts
#This shows the difference in Population figures between the "split Policy" data set.
arcpy.analysis.Statistics("AlpineBufferUnionInsideNonSplit", r"C:\Users\Kyle\Desktop\Temp\UnionDebug\UnionDebug.gdb\AlpineBufferUnionInsideNonSplit_Stat", "why_csv_Total_population SUM", None)

#Print the total of Population from the Sumation of the Census Tracts Populations from above
fc = "AlpineBufferUnionInsideNonSplit_Stat"
totPop = "Sum_why_csv_Total_population"
cursor = arcpy.SearchCursor(fc)
for rowdemand in cursor:
    totalPopulationInsideBuffer = (rowdemand.getValue(totPop))
print("Total Population from REGULAR Census Tracts:", totalPopulationInsideBuffer)