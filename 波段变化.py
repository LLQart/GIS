from osgeo import gdal_array

src = "FalseColor.tif"

arr = gdal_array.LoadFile(src)

output = gdal_array.SaveArray(arr[[1,0,2],:], "swap.tif", format="GTiff", prototype=src)


output =None