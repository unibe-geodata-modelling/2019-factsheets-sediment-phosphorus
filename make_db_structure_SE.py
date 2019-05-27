# create a database folder structure that looks like follows:
#(as and example the region Frienisberg is taken, but the structure stays the same for the
# regions Lobsigen, Schwanden, Seedorf and Suberg)
#
#Sedimenteintrag
#   Frienisberg
#       Frienisberg_1997_2007
#           Periode
#               Einzel
#               Summe
#               Mittel
#           Jahr
#               1997
#                 Einzel
#                 Summe
#               1998...
#           Datum
#               1998_02_25
#                   Einzel
#                   Summe
#                1998_03_21...
#           Erosionsform
#               linear
#                   Einzel
#                   Summe
#               flaechenhaft
#                   Einzel
#                   Summe
#           Parzelle
#               Parzelle_01
#                   Einzel
#                   Summe
#               Parzelle_02...
#       Frienisberg_2007_2017...(same as for Frienisberg_1997_2007)

#remark: the message "path already exists" might pop up sometimes even though new folders were created -> check this afterwards!

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

####################################################################################################################
# insert your paths here:

# where should the treelike folder structure start on your device?
Gebiete = r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag"

# where did you store the helping script on your device?
sys.path.insert(0, r'E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\Hilfsskripts')
import build_df_from_arcpy_181119 #ignore that python marks that line red!!!

# where did you store the input vector data on your device?
SE_vec_copied = r"E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied"

# where did you store the raster input data on your device?
SE_rasters = r"E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE"
####################################################################################################################

########### tree-branch "Periode"

#################################### create folders like Frienisberg_1997_2007/Periode/Einzel #####################
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)

    if os.path.exists(os.path.join(str(geb)+"_1997_2007","Periode","Einzel")):
        print("path already exists")
    else:
        new_dir_p1 = os.makedirs(os.path.join(str(geb) + "_1997_2007", "Periode", "Einzel"))

    if os.path.exists(os.path.join(str(geb)+"_2007_2017","Periode","Einzel")):
        print("path already exists")
    else:
        new_dir_p2 = os.makedirs(os.path.join(str(geb) + "_2007_2017", "Periode", "Einzel"))

#################################### create folders like Frienisberg_1997_2007/Periode/Summe #####################
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)

    if os.path.exists(os.path.join(str(geb)+"_1997_2007","Periode","Summe")):
        print("path already exists")
    else:
        new_dir_p1 = os.makedirs(os.path.join(str(geb) + "_1997_2007", "Periode", "Summe"))

    if os.path.exists(os.path.join(str(geb)+"_2007_2017","Periode","Summe")):
        print("path already exists")
    else:
        new_dir_p2 = os.makedirs(os.path.join(str(geb) + "_2007_2017", "Periode", "Summe"))

#################################### create folders like Frienisberg_1997_2007/Periode/Mittel #####################
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)

    if os.path.exists(os.path.join(str(geb)+"_1997_2007","Periode","Mittel")):
        print("path already exists")
    else:
        new_dir_p1 = os.makedirs(os.path.join(str(geb) + "_1997_2007", "Periode", "Mittel"))

    if os.path.exists(os.path.join(str(geb)+"_2007_2017","Periode","Mittel")):
        print("path already exists")
    else:
        new_dir_p2 = os.makedirs(os.path.join(str(geb) + "_2007_2017", "Periode", "Mittel"))

########### tree-branch "Jahr"
# (strictly, the period 1997-2007 starts in 1998 and 2007-2017 in 2008, so there are no events in 1997 and 2007 -> same naming convention as
# in the soil erosion database (which was given) was chosen)

#################################### create folders like Frienisberg_1997_2007/Jahr/1998/Einzel #####################

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
for vec_gb_p in origin_list:
    #list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
    arcpy.env.workspace = vec_gb_p
    vec_List = arcpy.ListFeatureClasses()

    cnt = 0
    for vec in vec_List:
        # extract Date form pandas dataframe and convert it to str
        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
        dat_1 = tab["Datum"][0]

        #because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
        # -> make strings out of them
        if type(dat_1) == str:
            dat_1 = dat_1
        elif isinstance(dat_1,pd.Timestamp) == True:
            dat_1 = str(pd.Timestamp.date(dat_1))

        #extract year
        year_1 = dat_1[:-6]

        # move year_1 in year_List
        if cnt == 0:
            year_List = [] + [year_1]
            cnt += 1
        else:
            year_List.append(year_1)

    #list that contains all of the years of vectors (where sediment input occured) of e.g. Frienisberg_07_17
    print(year_List)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    year_List = list(dict.fromkeys(year_List))
    print(year_List)

    # make new subdirectories Datum/year/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename of SE_vectors_copied folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Jahr/Jahr(e.g.2008)/Einzel
            if geb_p_name == os.path.basename(vec_gb_p):
                for d in year_List:
                    if os.path.exists(os.path.join(path_geb_p, "Jahr", d, "Einzel")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Jahr", d, "Einzel"))

#################################### create folders like Frienisberg_1997_2007/Jahr/1998/Summe #####################

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
for vec_gb_p in origin_list:
    #list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
    arcpy.env.workspace = vec_gb_p
    vec_List = arcpy.ListFeatureClasses()

    cnt = 0
    for vec in vec_List:
        # extract Date form pandas dataframe and convert it to str
        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
        dat_1 = tab["Datum"][0]

        #because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
        # -> make strings out of them
        if type(dat_1) == str:
            dat_1 = dat_1
        elif isinstance(dat_1,pd.Timestamp) == True:
            dat_1 = str(pd.Timestamp.date(dat_1))

        #extract year
        year_1 = dat_1[:-6]

        # move year_1 in year_List
        if cnt == 0:
            year_List = [] + [year_1]
            cnt += 1
        else:
            year_List.append(year_1)

    #list that contains all of the years of vectors (where sediment input occured) of e.g. Frienisberg_07_17
    print(year_List)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    year_List = list(dict.fromkeys(year_List))
    print(year_List)

    # make new subdirectories Datum/year/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename of SE_vectors_copied folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Jahr/Jahr(e.g.2008)/Summe
            if geb_p_name == os.path.basename(vec_gb_p):
                for d in year_List:
                    if os.path.exists(os.path.join(path_geb_p, "Jahr", d, "Summe")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Jahr", d, "Summe"))

###################### create folders like Frienisberg_1997_2007/Datum/2008_04_16/Einzel #####################

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
for vec_gb_p in origin_list:
    #list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
    arcpy.env.workspace = vec_gb_p
    vec_List = arcpy.ListFeatureClasses()

    cnt = 0
    for vec in vec_List:
        # extract Date form pandas dataframe and convert it to str
        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
        dat_1 = tab["Datum"][0]

        #because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
        # -> make strings out of them
        if type(dat_1) == str:
            dat_1 = dat_1
        elif isinstance(dat_1,pd.Timestamp) == True:
            dat_1 = str(pd.Timestamp.date(dat_1))

        # replace "-" witch "_"
        dat_1 = dat_1.replace('-', '_')

        # move dat_1 in date_List
        if cnt == 0:
            date_List = [] + [dat_1]
            cnt += 1
        else:
            date_List.append(dat_1)

    #list that contains all of the dates of vectors (where sediment input occured) of e.g. Frienisberg_07_17
    print(date_List)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    date_List = list(dict.fromkeys(date_List))
    print(date_List)

    # make new subdirectories Datum/date/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename of SE_vectors_copied folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Datum/date(e.g.2008_04_16)/Einzel
            if geb_p_name == os.path.basename(vec_gb_p):
                for d in date_List:
                    if os.path.exists(os.path.join(path_geb_p, "Datum", d, "Einzel")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Datum", d, "Einzel"))

###################### create folders like Frienisberg_1997_2007/Datum/2008_04_16/Summe #####################

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
for vec_gb_p in origin_list:
    #list vectors in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\SE_vectors_copied\Frienisberg_07_17
    arcpy.env.workspace = vec_gb_p
    vec_List = arcpy.ListFeatureClasses()

    cnt = 0
    for vec in vec_List:
        # extract Date form pandas dataframe and convert it to str
        tab = build_df_from_arcpy_181119.build_df_from_arcpy(os.path.join(vec_gb_p, vec))
        dat_1 = tab["Datum"][0]

        #because some date are strings and some are Timestamps (I don't know why...were digitalized like this), do distinguish between those data types
        # -> make strings out of them
        if type(dat_1) == str:
            dat_1 = dat_1
        elif isinstance(dat_1,pd.Timestamp) == True:
            dat_1 = str(pd.Timestamp.date(dat_1))

        # replace "-" witch "_"
        dat_1 = dat_1.replace('-', '_')

        # move dat_1 in date_List
        if cnt == 0:
            date_List = [] + [dat_1]
            cnt += 1
        else:
            date_List.append(dat_1)

    #list that contains all of the dates of vectors (where sediment input occured) of e.g. Frienisberg_07_17
    print(date_List)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    date_List = list(dict.fromkeys(date_List))
    print(date_List)

    # make new subdirectories Datum/date/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename of SE_vectors_copied folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Datum/date(e.g.2008_04_16)/Summe
            if geb_p_name == os.path.basename(vec_gb_p):
                for d in date_List:
                    if os.path.exists(os.path.join(path_geb_p, "Datum", d, "Summe")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Datum", d, "Summe"))

########### tree-branch "Parzelle"

#################################### create folders like Frienisberg_1997_2007/Parzelle/Parzelle_01/Einzel #####################

# make a list that consists of paths of SE_rasters-subfolders
count = 0
for SE_ras in os.listdir(SE_rasters):
    path_origin = os.path.join(SE_rasters, SE_ras)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)


for ras_gb_p in origin_list:
    #list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
    arcpy.env.workspace = ras_gb_p
    ras_List = arcpy.ListRasters()

    #write letter 6 and 7 of raster's name in a new list called parzelle_List
    cnt = 0
    for ras in ras_List:
        parzelle = "Parzelle_" + ras[5:7]

        # move parzelle in parzelle_List
        if cnt == 0:
            parzelle_List = [] + [parzelle]
            cnt += 1
        else:
            parzelle_List.append(parzelle)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    parzelle_List = list(dict.fromkeys(parzelle_List))
    print(parzelle_List)

    # make new subdirectories Parzelle/e.g. Parzelle_01/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename[:-3] of SE_rasters folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Parzelle/e.g.Parzelle_01/Einzel
            if geb_p_name == (os.path.basename(ras_gb_p)[:-3]):
                for d in parzelle_List:
                    if os.path.exists(os.path.join(path_geb_p, "Parzelle", d, "Einzel")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Parzelle", d, "Einzel"))

################################### create folders like Frienisberg_1997_2007/Parzelle/Parzelle_01/Summe #####################

# make a list that consists of paths of SE_rasters-subfolders
count = 0
for SE_ras in os.listdir(SE_rasters):
    path_origin = os.path.join(SE_rasters, SE_ras)

    if count == 0:
        origin_list = [] + [path_origin]
        count += 1
    else:
        origin_list.append(path_origin)

print(origin_list)


for ras_gb_p in origin_list:
    #list rasters in e.g. E:\David_Remund_Masterarbeit\alle_GE_MA\output_GE\Frienisberg_07_17_GE
    arcpy.env.workspace = ras_gb_p
    ras_List = arcpy.ListRasters()

    #write letter 6 and 7 of raster's name in a new list called parzelle_List
    cnt = 0
    for ras in ras_List:
        parzelle = "Parzelle_" + ras[5:7]

        # move parzelle in parzelle_List
        if cnt == 0:
            parzelle_List = [] + [parzelle]
            cnt += 1
        else:
            parzelle_List.append(parzelle)

    # remove duplicates out of a list -> in dictionary, no duplicates are allowed
    parzelle_List = list(dict.fromkeys(parzelle_List))
    print(parzelle_List)

    # make new subdirectories Parzelle/e.g. Parzelle_01/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones
    for geb in os.listdir(Gebiete):
        path_geb = os.path.join(Gebiete, geb)
        os.chdir(path_geb)

        for geb_p in os.listdir(path_geb):
            path_geb_p = os.path.join(path_geb, geb_p)

            path_geb_p_base = os.path.basename(path_geb_p)
            geb_p_name = path_geb_p_base.partition('_')[0] + "_" + path_geb_p_base[-7:-5] + "_" + path_geb_p_base[-2:]
            print(geb_p_name)

            # if geb_p_name (e.g. from Sedimenteintrag/Seedorf/Seedorf_2007_2017, it's Seedorf_07_17) is equal to basename[:-3] of SE_rasters folder, then create
            # new directories -> Sedimenteintrag/Seedorf/Seedorf_2007_2017  new is /Parzelle/e.g.Parzelle_01/Summe
            if geb_p_name == (os.path.basename(ras_gb_p)[:-3]):
                for d in parzelle_List:
                    if os.path.exists(os.path.join(path_geb_p, "Parzelle", d, "Summe")):
                        print("path already exists")
                    else:
                        new_dir = os.makedirs(os.path.join(path_geb_p, "Parzelle", d, "Summe"))

########### tree-branch "Erosionsform"

#################################### create folders like Frienisberg_1997_2007/Erosionsform/linear/Einzel #####################
# make new subdirectories Erosionsform/linear/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones

for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)

    for geb_p in os.listdir(path_geb):
        path_geb_p = os.path.join(path_geb, geb_p)
        print(path_geb_p)

        # make new subdirectories Erosionsform/linear/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007
        if os.path.exists(os.path.join(path_geb_p, "Erosionsform", "linear", "Einzel")):
            print("path already exists")
        else:
            new_dir = os.makedirs(os.path.join(path_geb_p, "Erosionsform", "linear", "Einzel"))

#################################### create folders like Frienisberg_1997_2007/Erosionsform/linear/Summe #####################
# make new subdirectories Erosionsform/linear/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones

for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)

    for geb_p in os.listdir(path_geb):
        path_geb_p = os.path.join(path_geb, geb_p)
        print(path_geb_p)

        # make new subdirectories Erosionsform/linear/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007
        if os.path.exists(os.path.join(path_geb_p, "Erosionsform", "linear", "Summe")):
            print("path already exists")
        else:
            new_dir = os.makedirs(os.path.join(path_geb_p, "Erosionsform", "linear", "Summe"))

#################################### create folders like Frienisberg_1997_2007/Erosionsform/flaechenhaft/Einzel #####################
# make new subdirectories Erosionsform/flaechenhaft/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones

for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)

    for geb_p in os.listdir(path_geb):
        path_geb_p = os.path.join(path_geb, geb_p)
        print(path_geb_p)

        # make new subdirectories Erosionsform/flaechenhaft/Einzel in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007
        if os.path.exists(os.path.join(path_geb_p, "Erosionsform", "flaechenhaft", "Einzel")):
            print("path already exists")
        else:
            new_dir = os.makedirs(os.path.join(path_geb_p, "Erosionsform", "flaechenhaft", "Einzel"))

#################################### create folders like Frienisberg_1997_2007/Erosionsform/flaechenhaft/Summe #####################
# make new subdirectories Erosionsform/flaechenhaft/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007 and similar ones

for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)

    for geb_p in os.listdir(path_geb):
        path_geb_p = os.path.join(path_geb, geb_p)
        print(path_geb_p)

        # make new subdirectories Erosionsform/flaechenhaft/Summe in e.g this path Sedimenteintrag\Frienisberg\Frienisberg_1997_2007
        if os.path.exists(os.path.join(path_geb_p, "Erosionsform", "flaechenhaft", "Summe")):
            print("path already exists")
        else:
            new_dir = os.makedirs(os.path.join(path_geb_p, "Erosionsform", "flaechenhaft", "Summe"))


#one strange folder was produced...delete this folder at the end!!!

if os.path.exists(r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Suberg\Suberg_1997_2007\Parzelle\Parzelle_ar"):
    arcpy.Delete_management(r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag\Suberg\Suberg_1997_2007\Parzelle\Parzelle_ar")
    print("strange folder got deleted")
else:
    print("no strange folder")


