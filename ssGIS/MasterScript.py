import arcpy
# :-)

# make the map a NAD 1983 UTM Zone 12N so you don't get weird projections

#environment prep?....I cant get this to work...at least I don't know what I am doing

# Delete Previous Feature Classes when working through the code
def CleanUp Script

# DEMOGRAPHICS PREP

# Learn to switch out abstract titles for something more descriptive
# Get rid of the extra weight columns I don't care about
# Get renter data
# Get # of Households
# Get Household income
# Times the pop figures by the county growth rate from 2015 to 2017 (or 2016)

# get rid of deadweight through the select by attribute script
# Eliminate unnecessary Census Tracts (just the county in question)
def SelectByAttribute Script

# join ACS data to Shapefiles
def Join Tool Script

# Create new Layer that can get a portion of the demographics from the census tl_2016_49_tract_STATEFP
def Ratio Demograph Script



# ITERATE THROUGH THE COMPETITION FEATURES...THIS WILL CREATE THE FILTER FOR PARCEL ANALYSIS
FOR LOOP to go through the features of the competition

# Use a WHILE LOOP to grow the Buffer until 95% of Supplied NetSFm (SuppNetSF95Occ) of the facility is <= the demandedSF of the Population (CompCapDemSF)
WHILE LOOP CODE
    Grow the radius of the Buffer

# Create Buffers
def BufferTool script

# Create Unions
def Union Script

# Use a dictionary python code script to sum the Population
# Times TotPop x 7.93 (Utah) to come up with Competition Captured DemandedSF (CompCapDemSF)
if SuppNetSF95Occ <= CompCapDemSF:
   def MakeFeatureLayer Script (this is the left over Demographic Tract Info)
   else def Delete NotBigEnough script (get rid of buffers and unions)

End Loop when the last Feature is done


# Use a dictionary/lookup table to select only the allowed zones
def ZoningLookUpTable Script
# Get rid of unnecessary zones geometery
def SelectByAttribute Script

# Spatial Join between the Zones and the Parcels
def SpatialJoin script
# Get rid of parcel that aren't zoned correctly
def MakeFeatureLayer Script (only keep the spatially joined parcels)


# RANK THE PARCELS
# want 60,000 people
# want 35% renters
# want traffic counts
# confirm household income
def Parcel Rank Script





#
