# copy the phospohorus input rasters at the *positions in the following database structure:
#(the *Einzel rasters were already calculated beforehand...*Summe and *Mittel have to be calculated sometimes before copying is possible...)
#(as and example the region Frienisberg is taken, but the structure stays the same for the
# regions Lobsigen, Schwanden, Seedorf and Suberg)
#
#Sedimenteintrag
#   Frienisberg
#       Frienisberg_1997_2007
#           Periode
#               *Einzel
#               *Summe
#               *Mittel
#           Jahr
#               1997
#                 *Einzel
#                 *Summe
#               1998...
#           Datum
#               1998_02_25
#                   *Einzel
#                   *Summe
#                1998_03_21...
#           Erosionsform
#               linear
#                   *Einzel
#                   *Summe
#               flaechenhaft
#                   *Einzel
#                   *Summe
#           Parzelle
#               Parzelle_01
#                   *Einzel
#                   *Summe
#               Parzelle_02...
#       Frienisberg_2007_2017...(same as for Frienisberg_1997_2007)

import os
import xlrd
import arcpy
from arcpy.sa import *
import numpy as np
import pandas as pd
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
import sys

# this is the folder, where the database treelike structure is bulit in
#(in this Folder the subfolders "Frienisberg", "Lobsigen", "Schwanden", "Seedorf", "Suberg" already existed)
Gebiete = r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Phosphoreintrag"

#get list of origin_folder paths (e.g. Frienisberg_97_07_PE where all the phosphorus input rasters are)
sed_inp_dir = r"E:\David_Remund_Masterarbeit\alle_GE_MA\output_P"

######### code until here as to be in the python console to RUN the Subsections of Code successfully ###################

####tree branch periode
############################  copy phosphorus input rasters to .../Periode/Einzel ################################
count = 0

for sed_geb in os.listdir(sed_inp_dir):
    path_origin = os.path.join(sed_inp_dir,sed_geb)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)

#get a list of all destination path folders
count = 0

for GEB in os.listdir(Gebiete):
    sub_GEB = os.listdir(os.path.join(Gebiete, GEB))

    for sub_geb in sub_GEB:
        #get destination name
        destination_path = os.path.join(Gebiete,GEB,sub_geb,"Periode","Einzel")
        print(destination_path)

        if count == 0:
            destination_list = [] + [destination_path]
            count += 1
        else:
            destination_list.append(destination_path)

print(destination_list)

#copy e.g. phosphorus input rasters of Frienisberg_07_17_PE to new created folder Frienisberg/Frienisberg_2007_2017/Periode/Einzel

for org in origin_list:
    for des in destination_list:
        #for origin path, get e.g. Seedorf17 out of r'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\output_GE\\Seedorf_07_17_SE'
        org_base = os.path.basename(org)
        org_name = org_base.partition('_')[0] + org_base[-5:-3]

        #for destination path, get e.g. Seedorf17 out of "E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Seedorf\\Seedorf_2007_2017\\Periode\\Einzel"
        des_gb_p = os.path.normpath(des)
        des_gb_p = des.split(os.sep)[6]
        des_name = des_gb_p.partition('_')[0] + des_gb_p[-2:]

        if org_name == des_name:
            #list all rasters in origin_path
            arcpy.env.workspace = org
            rasList = arcpy.ListRasters()

            for ras in rasList:
                if os.path.exists(os.path.join(des, ras)):
                    print("path already exists")
                else:
                    arcpy.Copy_management(ras,os.path.join(des,ras))
                    print(ras + " copied")

############################  copy sediment input rasters to .../Periode/Mittel ################################

#directory where mean sediment input rasters are, e.g. Frienisberg_07_17_SE.tif
sed_mean_dir = r"E:\David_Remund_Masterarbeit\alle_GE_MA\mean_P_input_Wilke"

#make a list of the paths of mean sediment input rasters
arcpy.env.workspace = sed_mean_dir
ras_list = arcpy.ListRasters()

count = 0
for ras in ras_list:
    path_origin = os.path.join(sed_mean_dir, ras)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)
print(origin_list)

# make a list of destination paths
count = 0
for GEB in os.listdir(Gebiete):
    sub_GEB = os.listdir(os.path.join(Gebiete, GEB))

    for sub_geb in sub_GEB:
        #get destination name
        destination_path = os.path.join(Gebiete,GEB,sub_geb,"Periode","Mittel")

        if count == 0:
            destination_list = [] + [destination_path]
            count += 1
        else:
            destination_list.append(destination_path)

print(destination_list)

#copy e.g. sediment input rasters of Frienisberg_07_17_SE to new created folder Frienisberg/Frienisberg_2007_2017/Periode/Mittel
for org in origin_list:
    for des in destination_list:
        #for origin path, get e.g. Seedorf17 out of r'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\output_GE\\Seedorf_07_17_SE'
        org = os.path.basename(org)
        org_part = org.partition('_')[2]
        org_name = org_part.partition('_')[0] + org[-9:-7]
        print(org_name)

        #for destination path, get e.g. Seedorf17 out of "E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Seedorf\\Seedorf_2007_2017\\Periode\\Mittel"
        des_gb_p = os.path.normpath(des)
        des_gb_p = des.split(os.sep)[6]
        des_name = des_gb_p.partition('_')[0] + des_gb_p[-2:]
        print(des_name)

        #if orgin name (org_name) equals destination name (des_name, e.g. Seedorf17), then copy:
        if org_name == des_name:
            arcpy.env.workspace = org
            if os.path.exists(os.path.join(des, os.path.basename(org))):
                print("file already exists")
            else:
                arcpy.Copy_management(org,os.path.join(des, os.path.basename(org)))
                print(org + " copied to " + os.path.join(des, os.path.basename(org)))

#################### sum up .../Peiode/Einzel rasters and copy sediment input rasters to .../Periode/Summe ###########

#make a list of raster-folders path e.g. .../Frienisberg_1997_2007/Periode/Einzel
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_origin = os.path.join(path_geb,GEB,"Periode","Einzel")

        if count == 0:
            origin_list = [] + [path_origin]
            count += 1
        else:
            origin_list.append(path_origin)
print(origin_list)

#for all rasters in e.g. .../Frienisberg_1997_2007/Periode/Einzel, calculate mean of all rasters and
#save sum raster in e.g. .../Frienisberg_1997_2007/Periode/Mittel
for org in origin_list:
    # set output Cooridnate-System -> otherwise, after NumpyToRaster Conversion, the Coordinate System is "unknown"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("CH1903 LV03")

    arcpy.env.workspace = org
    rasterList = arcpy.ListRasters()

    # pick first raster of list and extract location information out of it
    locate_raster = Raster(rasterList[0])

    # get lowerLeft and cellSize
    lowerLeft = arcpy.Point(locate_raster.extent.XMin, locate_raster.extent.YMin)
    cellSize = locate_raster.meanCellWidth

    i = 0
    for ras in rasterList:
        # sum up all rasters [t/ha] of e.g. .../Frienisberg_1997_2007/Periode/Einzel after conversion to numpy array
        arr = arcpy.RasterToNumPyArray(ras)
        arr = arr.astype(float)

        if i == 0:
            outras1 = arr
            i += 1
        else:
            outras1 = outras1 + arr
            i += 1
    # convert numpy array back to raster
    sum_ras = arcpy.NumPyArrayToRaster(outras1, lowerLeft, cellSize, cellSize)

    #extract out of the path .../Frienisberg_1997_2007/Periode/Einzel the string Frienisberg_97_07
    org_name = org.split(os.sep)[6]
    org_name = org_name.split('_')[0] + "_" + org_name[-7:-5] + "_" + org_name[-2:]

    # set new_basename for output path
    newbase_name = "sum_" + org_name + "_PE.tif"


    #get from path e.g. 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Periode\\Einzel'
    # the part 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Periode'
    # and add //Summe to the extracted path
    destination_path = os.path.dirname(org)
    destination_path = os.path.join(destination_path,"Summe",newbase_name)



    # save sum_ras in the destination path if the destination file doesn't already exist
    if os.path.exists(destination_path):
        print("file already exists")
    else:
        sum_ras.save(destination_path)
        print(sum_ras)

####tree branch Jahr
############################  copy sediment input rasters to .../Jahr/e.g.1998/Einzel ################################

#script for converting GIS attribute table to pandas dataframe
sys.path.insert(0, r'E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\Hilfsskripts')
import build_df_from_arcpy_181119 #ignore that python marks that line red!!!

#folder that was created through the script "copy_SE_vectors.py" -> for more information, read documentation of copy_SE_vectors.py
SE_vec_copied = r"E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied"

# make a list that consists of paths of SE_vectors_copies-subfolders
count = 0
for SE_vec in os.listdir(SE_vec_copied):
    path_origin = os.path.join(SE_vec_copied, SE_vec)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)

count = 0
#make a list of raster-folders path e.g. ...output_GE/Frienisberg_07_17_GE (sed_inp_dir has to be in Console)
for sed_geb in os.listdir(sed_inp_dir):
    path_origin = os.path.join(sed_inp_dir,sed_geb)

    if count == 0:
        sed_inp_list = [] + [path_origin]
        count += 1
    else:
        sed_inp_list.append(path_origin)

print(sed_inp_list)

for se in sed_inp_list:
    for vec_gb_p in origin_list:
        # list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
        arcpy.env.workspace = vec_gb_p
        vec_List = arcpy.ListFeatureClasses()

        # list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
        arcpy.env.workspace = se
        se_List = arcpy.ListRasters()

        # e.g. the event FEKRE31_M2_024_SE.tif is ONLY unique in a specific region -> the event FEKRE31_M2_024_SE.tif
        # exists in Frienisberg_97_07 AND in Lobisgen_97_07
        #
        #therefore only copy a sediment input raster if the raster is in the same region as the correpsonding vector
        if os.path.basename(se[:-3]) == os.path.basename(vec_gb_p):

            for ras in se_List:
                for vec in vec_List:
                    if ras[:-7] == vec[:-4]:
                        print(ras)

                        # extract Date form pandas dataframe and convert it to str
                        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
                        dat_1 = tab["Datum"][0]

                        # because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
                        # -> make strings out of them
                        if type(dat_1) == str:
                            dat_1 = dat_1
                        elif isinstance(dat_1, pd.Timestamp) == True:
                            dat_1 = str(pd.Timestamp.date(dat_1))

                        # extract year
                        year_1 = dat_1[:-6]
                        print(year_1)

                        # copy the corresponding raster to new directory: e.g.
                        # E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Frienisberg\Frienisberg_1997_2007\Jahr\1998\Einzel

                        if os.path.basename(vec_gb_p)[-5:] == "07_17":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_2007_2017", "Jahr",
                                                            year_1,
                                                            "Einzel")
                        if os.path.basename(vec_gb_p)[-5:] == "97_07":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_1997_2007", "Jahr",
                                                            year_1,
                                                            "Einzel")

                        # copy the sediment input raster (ras) to the destination path folder
                        if os.path.exists(os.path.join(destination_path, ras)):
                            print("file already exists")  # file can also be already copied in the same RUN session

                        else:
                            arcpy.Copy_management(ras, os.path.join(destination_path, ras))
                            print(ras + " copied to " + os.path.join(destination_path, ras))

############################ calculate yearly sum  & copy sum raster to .../Jahr/e.g.1998/Summe ################
# note: the yearly sum in [t/ha] has the same value as the yearly mean in [t/ha*a] (because of division through 1a)

### calculate yearly sum of sediment input rasters in e.g. ...\Frienisberg_1997_2007\Jahr\1998\Einzel & copy
#   the sum raster to e.g. ...\Frienisberg_1997_2007\Jahr\1998\Summe    #####################################

#make a list of paths like e.g. ...\Frienisberg_1997_2007\Jahr\e.g.1998\Einzel
count = 0
for GEB in os.listdir(Gebiete):
    sub_GEB = os.path.join(Gebiete, GEB)

    for sub_geb in os.listdir(sub_GEB):
        Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Jahr")

        for Jahr in os.listdir(Jahr_path):
            specific_Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Jahr",Jahr,"Einzel")

            if count == 0:
                specific_Jahr_list = [] + [specific_Jahr_path]
                count += 1
            else:
                specific_Jahr_list.append(specific_Jahr_path)

print(specific_Jahr_list)

#sum up all sediment input rasters in folders with paths like e.g. ...\Frienisberg_1997_2007\Jahr\e.g.1998\Einzel
for SE_ras in specific_Jahr_list:
    # set output Cooridnate-System -> otherwise, after NumpyToRaster Conversion, the Coordinate System is "unknown"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("CH1903 LV03")

    arcpy.env.workspace = SE_ras
    rasterList = arcpy.ListRasters()

    # pick first raster of list and extract location information out of it
    locate_raster = Raster(rasterList[0])

    # get lowerLeft and cellSize
    lowerLeft = arcpy.Point(locate_raster.extent.XMin, locate_raster.extent.YMin)
    cellSize = locate_raster.meanCellWidth

    i = 0
    for ras in rasterList:
        # sum up all rasters [t/ha] of e.g. .../Frienisberg_1997_2007/Jahr/e.g.1998/Einzel after conversion to numpy array
        arr = arcpy.RasterToNumPyArray(ras)
        arr = arr.astype(float)

        if i == 0:
            outras1 = arr
            i += 1
        else:
            outras1 = outras1 + arr
            i += 1

    # convert numpy array back to raster
    sum_ras = arcpy.NumPyArrayToRaster(outras1, lowerLeft, cellSize, cellSize)

    ##########set the new_basename e.g. sum_Frienisberg_97_07_1998_SE.tif ################

    # extract out of the path .../Frienisberg_1997_2007/Jahr/1998/Einzel the string Frienisberg_97_07
    gebperi_name = SE_ras.split(os.sep)[6]
    gebperi_name = gebperi_name.split('_')[0] + "_" + gebperi_name[-7:-5] + "_" + gebperi_name[-2:]

    # extract out of the path .../Frienisberg_1997_2007/Jahr/1998/Einzel the Jahr-string
    year = SE_ras.split(os.sep)[8]

    # set new_basename for output path
    newbase_name = "sum_" + gebperi_name + "_"+ year + "_PE.tif"
    print(newbase_name)

    ############# copy sum_raster to the destination path ###############

    # get from path e.g. 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Jahr\\some year\\Einzel'
    # the part 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Jahr\\some year'
    # and add //Summe to the extracted path
    destination_path = os.path.dirname(SE_ras)
    destination_path = os.path.join(destination_path, "Summe", newbase_name)

    # save sum_ras in the destination path if the destination file doesn't already exist
    if os.path.exists(destination_path):
        print("file already exists")
    else:
        sum_ras.save(destination_path)
        print(newbase_name + " was copied to " + destination_path)


####tree branch Datum
############################  copy sediment input rasters to .../Datum/e.g.1998_02_25/Einzel ################################

#script for converting GIS attribute table to pandas dataframe
sys.path.insert(0, r'E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\Hilfsskripts')
import build_df_from_arcpy_181119 #ignore that python marks that line red!!!

#folder that was created through the script "copy_SE_vectors.py" -> for more information, read documentation of copy_SE_vectors.py
SE_vec_copied = r"E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied"

# make a list that consists of paths of SE_vectors_copies-subfolders
count = 0
for SE_vec in os.listdir(SE_vec_copied):
    path_origin = os.path.join(SE_vec_copied, SE_vec)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)

count = 0
#make a list of raster-folders path e.g. ...output_GE/Frienisberg_07_17_GE (sed_inp_dir has to be in Console)
for sed_geb in os.listdir(sed_inp_dir):
    path_origin = os.path.join(sed_inp_dir,sed_geb)

    if count == 0:
        sed_inp_list = [] + [path_origin]
        count += 1
    else:
        sed_inp_list.append(path_origin)

print(sed_inp_list)

for se in sed_inp_list:
    for vec_gb_p in origin_list:
        # list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
        arcpy.env.workspace = vec_gb_p
        vec_List = arcpy.ListFeatureClasses()

        # list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
        arcpy.env.workspace = se
        se_List = arcpy.ListRasters()

        # e.g. the event FEKRE31_M2_024_SE.tif is ONLY unique in a specific region -> the event FEKRE31_M2_024_SE.tif
        # exists in Frienisberg_97_07 AND in Lobisgen_97_07
        #
        #therefore only copy a sediment input raster if the raster is in the same region as the correpsonding vector
        if os.path.basename(se[:-3]) == os.path.basename(vec_gb_p):

            for ras in se_List:
                for vec in vec_List:
                    if ras[:-7] == vec[:-4]:
                        print(ras)

                        # extract Date form pandas dataframe and convert it to str
                        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
                        dat_1 = tab["Datum"][0]

                        # because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
                        # -> make strings out of them
                        if type(dat_1) == str:
                            dat_1 = dat_1
                        elif isinstance(dat_1, pd.Timestamp) == True:
                            dat_1 = str(pd.Timestamp.date(dat_1))

                        dat_1 = dat_1.replace("-","_")


                        # copy the corresponding raster to new directory: e.g.
                        # E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Frienisberg\Frienisberg_1997_2007\Datum\1998_08_10\Einzel

                        if os.path.basename(vec_gb_p)[-5:] == "07_17":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_2007_2017", "Datum",
                                                            dat_1,
                                                            "Einzel")
                        if os.path.basename(vec_gb_p)[-5:] == "97_07":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_1997_2007", "Datum",
                                                            dat_1,
                                                            "Einzel")

                        # copy the sediment input raster (ras) to the destination path folder
                        if os.path.exists(os.path.join(destination_path, ras)):
                            print("file already exists")  # file can also be already copied in the same RUN session

                        else:
                            arcpy.Copy_management(ras, os.path.join(destination_path, ras))
                            print(ras + " copied to " + os.path.join(destination_path, ras))

############################ calculate date sum  & copy sum raster to .../Datum/e.g.1998_02_13/Summe ################

### calculate date sum of sediment input rasters in e.g. ...\Frienisberg_1997_2007\Datum\1998_02_13\Einzel & copy
#   the sum raster to e.g. ...\Frienisberg_1997_2007\Datum\1998_02_13\Summe    #####################################

#make a list of paths like e.g. ...\Frienisberg_1997_2007\Datum\e.g.1998_02_13\Einzel
count = 0
for GEB in os.listdir(Gebiete):
    sub_GEB = os.path.join(Gebiete, GEB)

    for sub_geb in os.listdir(sub_GEB):
        Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Datum")

        for Datum in os.listdir(Jahr_path):
            specific_Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Datum",Datum,"Einzel")

            if count == 0:
                specific_Jahr_list = [] + [specific_Jahr_path]
                count += 1
            else:
                specific_Jahr_list.append(specific_Jahr_path)

print(specific_Jahr_list)

#sum up all sediment input rasters in folders with paths like e.g. ...\Frienisberg_1997_2007\Datum\e.g.1998_02_13\Einzel
for SE_ras in specific_Jahr_list:
    # set output Cooridnate-System -> otherwise, after NumpyToRaster Conversion, the Coordinate System is "unknown"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("CH1903 LV03")

    arcpy.env.workspace = SE_ras
    rasterList = arcpy.ListRasters()

    # pick first raster of list and extract location information out of it
    locate_raster = Raster(rasterList[0])

    # get lowerLeft and cellSize
    lowerLeft = arcpy.Point(locate_raster.extent.XMin, locate_raster.extent.YMin)
    cellSize = locate_raster.meanCellWidth

    i = 0
    for ras in rasterList:
        # sum up all rasters [t/ha] of e.g. .../Frienisberg_1997_2007/Jahr/e.g.1998/Einzel after conversion to numpy array
        arr = arcpy.RasterToNumPyArray(ras)
        arr = arr.astype(float)

        if i == 0:
            outras1 = arr
            i += 1
        else:
            outras1 = outras1 + arr
            i += 1

    # convert numpy array back to raster
    sum_ras = arcpy.NumPyArrayToRaster(outras1, lowerLeft, cellSize, cellSize)

    ##########set the new_basename e.g. sum_Frienisberg_97_07_1998_SE.tif ################

    # extract out of the path .../Frienisberg_1997_2007/Jahr/1998/Einzel the string Frienisberg_97_07
    gebperi_name = SE_ras.split(os.sep)[6]
    gebperi_name = gebperi_name.split('_')[0] + "_" + gebperi_name[-7:-5] + "_" + gebperi_name[-2:]

    # extract out of the path .../Frienisberg_1997_2007/Jahr/1998/Einzel the Jahr-string
    date = SE_ras.split(os.sep)[8]

    # set new_basename for output path
    newbase_name = "sum_" + gebperi_name + "_"+ date + "_PE.tif"
    print(newbase_name)

    ############# copy sum_raster to the destination path ###############

    # get from path e.g. 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Datum\\some date\\Einzel'
    # the part 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Datum\\some date'
    # and add //Summe to the extracted path
    destination_path = os.path.dirname(SE_ras)
    destination_path = os.path.join(destination_path, "Summe", newbase_name)

    # save sum_ras in the destination path if the destination file doesn't already exist
    if os.path.exists(destination_path):
        print("file already exists")
    else:
        sum_ras.save(destination_path)
        print(newbase_name + " was copied to " + destination_path)

####tree branch Erosionsform
############################  copy sediment input rasters to .../Erosionsform/linear or flaechenhaft/Einzel ############

#script for converting GIS attribute table to pandas dataframe
sys.path.insert(0, r'E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\Hilfsskripts')
import build_df_from_arcpy_181119 #ignore that python marks that line red!!!

#folder that was created through the script "copy_SE_vectors.py" -> for more information, read documentation of copy_SE_vectors.py
SE_vec_copied = r"E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied"

# make a list that consists of paths of SE_vectors_copies-subfolders
count = 0
for SE_vec in os.listdir(SE_vec_copied):
    path_origin = os.path.join(SE_vec_copied, SE_vec)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)

count = 0
#make a list of raster-folders path e.g. ...output_GE/Frienisberg_07_17_GE (sed_inp_dir has to be in Console)
for sed_geb in os.listdir(sed_inp_dir):
    path_origin = os.path.join(sed_inp_dir,sed_geb)

    if count == 0:
        sed_inp_list = [] + [path_origin]
        count += 1
    else:
        sed_inp_list.append(path_origin)

print(sed_inp_list)


for se in sed_inp_list:
    for vec_gb_p in origin_list:
        # list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
        arcpy.env.workspace = vec_gb_p
        vec_List = arcpy.ListFeatureClasses()

        # list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
        arcpy.env.workspace = se
        se_List = arcpy.ListRasters()

        # e.g. the event FEKRE31_M2_024_SE.tif is ONLY unique in a specific region -> the event FEKRE31_M2_024_SE.tif
        # exists in Frienisberg_97_07 AND in Lobisgen_97_07
        #
        #therefore only copy a sediment input raster if the raster is in the same region as the correpsonding vector
        if os.path.basename(se[:-3]) == os.path.basename(vec_gb_p):

            for ras in se_List:
                for vec in vec_List:
                    if ras[:-7] == vec[:-4]:
                        print(ras)

                        # extract Erosionsform form pandas dataframe and convert it to str
                        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
                        EroForm = tab["EroForm"][0]
                        print(EroForm)

                        if EroForm == "RE":
                            EroForm = "linear"
                        if EroForm == "RNE":
                            EroForm = "linear"
                        if EroForm == "FRE":
                            EroForm = "linear"
                        if EroForm == "FE":
                            EroForm = "flaechenhaft"
                        if EroForm == "KRE":
                            EroForm = "flaechenhaft"
                        print(EroForm)


                        # copy the corresponding raster to new directory: e.g.
                        # E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Frienisberg\Frienisberg_1997_2007\Erosionsform\linear oder flaechenhaft\Einzel

                        if os.path.basename(vec_gb_p)[-5:] == "07_17":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_2007_2017", "Erosionsform",
                                                            EroForm,
                                                            "Einzel")
                        if os.path.basename(vec_gb_p)[-5:] == "97_07":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_1997_2007", "Erosionsform",
                                                            EroForm,
                                                            "Einzel")

                        print(destination_path)

                        # copy the sediment input raster (ras) to the destination path folder
                        if os.path.exists(os.path.join(destination_path, ras)):
                            print("file already exists")  # file can also be already copied in the same RUN session

                        else:
                            arcpy.Copy_management(ras, os.path.join(destination_path, ras))
                            print(ras + " copied to " + os.path.join(destination_path, ras))

#######  calculate linear or areal sum & copy sum rasters to .../Erosionsform/linear or flaechenhaft/Summe ############

#make a list of paths like e.g. ...\Frienisberg_1997_2007\Erosionsform\linear oder flaechenhaft\Einzel
count = 0
for GEB in os.listdir(Gebiete):
    sub_GEB = os.path.join(Gebiete, GEB)

    for sub_geb in os.listdir(sub_GEB):
        Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Erosionsform")

        for EroF in os.listdir(Jahr_path):
            specific_Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Erosionsform",EroF,"Einzel")

            if count == 0:
                specific_Jahr_list = [] + [specific_Jahr_path]
                count += 1
            else:
                specific_Jahr_list.append(specific_Jahr_path)

print(specific_Jahr_list)

#remove ...\Seedorf_2007_2017\Erosionsform\flaechenhaft\Einzel out of the specific_Jahr_list (because there is no flaechenhaft sediment input)
del specific_Jahr_list[14]
print(len(specific_Jahr_list))

#sum up all sediment input rasters in folders with paths like e.g. ...\Frienisberg_1997_2007\Erosionsform\linear or flaechenhaft\Einzel
for SE_ras in specific_Jahr_list:
    # set output Cooridnate-System -> otherwise, after NumpyToRaster Conversion, the Coordinate System is "unknown"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("CH1903 LV03")

    arcpy.env.workspace = SE_ras
    rasterList = arcpy.ListRasters()

    # pick first raster of list and extract location information out of it
    locate_raster = Raster(rasterList[0])

    # get lowerLeft and cellSize
    lowerLeft = arcpy.Point(locate_raster.extent.XMin, locate_raster.extent.YMin)
    cellSize = locate_raster.meanCellWidth

    i = 0
    for ras in rasterList:
        # sum up all rasters [t/ha] of e.g. .../Frienisberg_1997_2007/Jahr/e.g.1998/Einzel after conversion to numpy array
        arr = arcpy.RasterToNumPyArray(ras)
        arr = arr.astype(float)

        if i == 0:
            outras1 = arr
            i += 1
        else:
            outras1 = outras1 + arr
            i += 1

    # convert numpy array back to raster
    sum_ras = arcpy.NumPyArrayToRaster(outras1, lowerLeft, cellSize, cellSize)

    ##########set the new_basename e.g. sum_Frienisberg_97_07_linear(or flaechenhaft)_SE.tif ################

    # extract out of the path e.g .../Frienisberg_1997_2007/Erosionsform/linear/Einzel the string Frienisberg_97_07
    gebperi_name = SE_ras.split(os.sep)[6]
    gebperi_name = gebperi_name.split('_')[0] + "_" + gebperi_name[-7:-5] + "_" + gebperi_name[-2:]

    # extract out of the path e.g. .../Frienisberg_1997_2007/Erosionsform/linear/Einzel the linear (or flaechenhaft)-string
    ero_Name = SE_ras.split(os.sep)[8]

    # set new_basename for output path
    newbase_name = "sum_" + gebperi_name + "_"+ ero_Name + "_PE.tif"
    print(newbase_name)

    ############# copy sum_raster to the destination path ###############

    # get from path e.g. 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Erosionsform\\linear or flaechenhaft\\Einzel'
    # the part 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Erosionsform\\linear or flaechenhaft'
    # and add //Summe to the extracted path
    destination_path = os.path.dirname(SE_ras)
    destination_path = os.path.join(destination_path, "Summe", newbase_name)
    print(destination_path)

    # save sum_ras in the destination path if the destination file doesn't already exist
    if os.path.exists(destination_path):
        print("file already exists")
    else:
        sum_ras.save(destination_path)
        print(newbase_name + " was copied to " + destination_path)

####tree branch Parzelle
############################  copy sediment input rasters to .../Parzelle/Parzellen-Nr, e.g.01/Einzel ############

#script for converting GIS attribute table to pandas dataframe
sys.path.insert(0, r'E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\Hilfsskripts')
import build_df_from_arcpy_181119 #ignore that python marks that line red!!!

#folder that was created through the script "copy_SE_vectors.py" -> for more information, read documentation of copy_SE_vectors.py
SE_vec_copied = r"E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied"

# make a list that consists of paths of SE_vectors_copies-subfolders
count = 0
for SE_vec in os.listdir(SE_vec_copied):
    path_origin = os.path.join(SE_vec_copied, SE_vec)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)

count = 0
#make a list of raster-folders path e.g. ...output_GE/Frienisberg_07_17_GE (sed_inp_dir has to be in Console)
for sed_geb in os.listdir(sed_inp_dir):
    path_origin = os.path.join(sed_inp_dir,sed_geb)

    if count == 0:
        sed_inp_list = [] + [path_origin]
        count += 1
    else:
        sed_inp_list.append(path_origin)

print(sed_inp_list)


for se in sed_inp_list:
    for vec_gb_p in origin_list:
        # list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
        arcpy.env.workspace = vec_gb_p
        vec_List = arcpy.ListFeatureClasses()

        # list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
        arcpy.env.workspace = se
        se_List = arcpy.ListRasters()

        # e.g. the event FEKRE31_M2_024_SE.tif is ONLY unique in a specific region -> the event FEKRE31_M2_024_SE.tif
        # exists in Frienisberg_97_07 AND in Lobisgen_97_07
        #
        #therefore only copy a sediment input raster if the raster is in the same region as the correpsonding vector
        if os.path.basename(se[:-3]) == os.path.basename(vec_gb_p):

            for ras in se_List:
                for vec in vec_List:
                    if ras[:-7] == vec[:-4]:

                        # extract Parzellen-Nr. form pandas dataframe and convert it to str
                        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
                        Parzellen_Nr = tab["Parzelle"][0]
                        Parzellen_Nr = str(Parzellen_Nr)

                        #there are 2 events that have field number 3536 and 4041 -> therefore: when Parzellen_Nr
                        #consists of 4 digits, only take the first 2 digits
                        if len(Parzellen_Nr) == 2:
                            Parzellen_Nr = Parzellen_Nr
                        if len(Parzellen_Nr) == 4:
                            Parzellen_Nr = Parzellen_Nr[:-2]

                        #write e.g. field number 1 as 01
                        Parzellen_Nr = Parzellen_Nr.zfill(2)

                        # copy the corresponding raster to new directory: e.g.
                        # E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Frienisberg\Frienisberg_1997_2007\Parzelle\e.g. 01\Einzel

                        if os.path.basename(vec_gb_p)[-5:] == "07_17":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_2007_2017", "Parzelle",
                                                            "Parzelle_"+Parzellen_Nr,
                                                            "Einzel")
                        if os.path.basename(vec_gb_p)[-5:] == "97_07":
                            destination_path = os.path.join(Gebiete, os.path.basename(vec_gb_p)[:-6],
                                                            os.path.basename(vec_gb_p)[:-6] + "_1997_2007", "Parzelle",
                                                            "Parzelle_" + Parzellen_Nr,
                                                            "Einzel")

                        # copy the sediment input raster (ras) to the destination path folder
                        if os.path.exists(os.path.join(destination_path, ras)):
                            print("file already exists")  # file can also be already copied in the same RUN session

                        else:
                            arcpy.Copy_management(ras, os.path.join(destination_path, ras))
                            print(ras + " copied to " + os.path.join(destination_path, ras))

############################  calculate Parzelle-sum & copy sum  rasters to
############################ .../Parzelle/Parzellen-Nr, e.g.01/Summe #########

#make a list of paths like e.g. ...\Frienisberg_1997_2007\Parzelle\e.g.01\Einzel
count = 0
for GEB in os.listdir(Gebiete):
    sub_GEB = os.path.join(Gebiete, GEB)

    for sub_geb in os.listdir(sub_GEB):
        Jahr_path = os.path.join(Gebiete,GEB,sub_geb,"Parzelle")

        for Parz in os.listdir(Jahr_path):
            parz_nr_path = os.path.join(Gebiete,GEB,sub_geb,"Parzelle",Parz,"Einzel")

            if count == 0:
                parz_nr_list = [] + [parz_nr_path]
                count += 1
            else:
                parz_nr_list.append(parz_nr_path)

print(parz_nr_list)


#sum up all sediment input rasters in folders with paths like e.g. ...\Frienisberg_1997_2007\Erosionsform\linear or flaechenhaft\Einzel
for SE_ras in parz_nr_list:
    # set output Cooridnate-System -> otherwise, after NumpyToRaster Conversion, the Coordinate System is "unknown"
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("CH1903 LV03")

    arcpy.env.workspace = SE_ras
    rasterList = arcpy.ListRasters()

    # pick first raster of list and extract location information out of it
    locate_raster = Raster(rasterList[0])

    # get lowerLeft and cellSize
    lowerLeft = arcpy.Point(locate_raster.extent.XMin, locate_raster.extent.YMin)
    cellSize = locate_raster.meanCellWidth

    i = 0
    for ras in rasterList:
        # sum up all rasters [t/ha] of e.g. .../Frienisberg_1997_2007/Jahr/e.g.1998/Einzel after conversion to numpy array
        arr = arcpy.RasterToNumPyArray(ras)
        arr = arr.astype(float)

        if i == 0:
            outras1 = arr
            i += 1
        else:
            outras1 = outras1 + arr
            i += 1

    # convert numpy array back to raster
    sum_ras = arcpy.NumPyArrayToRaster(outras1, lowerLeft, cellSize, cellSize)

    ##########set the new_basename e.g. sum_Frienisberg_97_07_P01_SE.tif ################

    # extract out of the path e.g .../Frienisberg_1997_2007/Erosionsform/linear/Einzel the string Frienisberg_97_07
    gebperi_name = SE_ras.split(os.sep)[6]
    gebperi_name = gebperi_name.split('_')[0] + "_" + gebperi_name[-7:-5] + "_" + gebperi_name[-2:]

    # extract out of the path e.g. .../Frienisberg_1997_2007/Parzelle/Parzelle_01/Einzel the 01-string
    parz_Name = (SE_ras.split(os.sep)[8])[-2:]

    # set new_basename for output path
    newbase_name = "sum_" + gebperi_name + "_P"+ parz_Name + "_PE.tif"
    print(newbase_name)

    ############# copy sum_raster to the destination path ###############

    # get from path e.g. 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Parzelle\\Parzelle_01\\Einzel'
    # the part 'E:\\David_Remund_Masterarbeit\\alle_GE_MA\\Gewässereintrag\\Sedimenteintrag\\Frienisberg\\Frienisberg_1997_2007\\Parzelle\\Parzelle_01'
    # and add //Summe to the extracted path
    destination_path = os.path.dirname(SE_ras)
    destination_path = os.path.join(destination_path, "Summe", newbase_name)
    print(destination_path)

    # save sum_ras in the destination path if the destination file doesn't already exist
    if os.path.exists(destination_path):
        print("file already exists")
    else:
        sum_ras.save(destination_path)
        print(newbase_name + " was copied to " + destination_path)


