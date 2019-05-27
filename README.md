# 2019-automated factsheets for sediment & phosphorus input into waterbodies
(based on a 20 year long soil erosion database in the region of Frienisberg, Switzerland)

Author: David Remund 13-104-591
University of Berne, Seminar Geodata analysis and modelling (Springsemester 2019)


# aim of the scripts:

The aim of the scripts is to make PDF overview sheets that show for so called region-period objects (e.g. Frienisberg 1997-2007) important information about sediment & phosphorus input.

# Methodical realization:

The aim is reached with 4 scripts. The first script makes a treelike output folder structure for the input data (which was already calculated beforehand in this case). The second script copies initial the sediment (phosphorus) input rasters to the right destination folder in the created treelike output folder structure. Some rasters are had to be summed up prior to the copying process. The third script checks if some "strange rasters" have been created during the copying process (probably these strange rasters are temporary storage files). If a strange raster should be detected, then this script deletes them. The fourth and last script calculates afterwards the total sum [t] and the mean annual input [t/ha*a] and makes boxplots as well as timeseries. All the calculated elements are drawn together on a PDF sheet.

# Used software:

The programming was done with Python 3.6 in the IDE PyCharm 2018.2.5 Community Edition.

