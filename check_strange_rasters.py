# check if the there are some strange rasters (probably temporary storage files) among the copied rasters
# check only in the Summe folders, because these strange can occur through the summing up process

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
Gebiete = r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag\Sedimenteintrag"

############################ check branch .../Frienisberg_1997_2007/Periode/Einzel ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Periode","Einzel")

        if count == 0:
            peri_einzel_list = [] + [path_p_einz]
            count += 1
        else:
            peri_einzel_list.append(path_p_einz)

print(peri_einzel_list)

for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Periode/Summe ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Periode","Summe")

        if count == 0:
            peri_einzel_list = [] + [path_p_einz]
            count += 1
        else:
            peri_einzel_list.append(path_p_einz)

print(peri_einzel_list)

for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Periode/Mittel ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Periode","Mittel")

        if count == 0:
            peri_einzel_list = [] + [path_p_einz]
            count += 1
        else:
            peri_einzel_list.append(path_p_einz)

print(peri_einzel_list)

for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Jahr/specific_year/Einzel ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Jahr")

        for year in os.listdir(path_p_einz):
            path_y_einz = os.path.join(path_p_einz,year,"Einzel")

            if count == 0:
                peri_einzel_list = [] + [path_y_einz]
                count += 1
            else:
                peri_einzel_list.append(path_y_einz)

print(peri_einzel_list)


for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Jahr/specific_year/Summe ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Jahr")

        for year in os.listdir(path_p_einz):
            path_y_einz = os.path.join(path_p_einz,year,"Summe")

            if count == 0:
                peri_einzel_list = [] + [path_y_einz]
                count += 1
            else:
                peri_einzel_list.append(path_y_einz)

print(peri_einzel_list)


for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Datum/specific_date/Einzel ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Datum")

        for year in os.listdir(path_p_einz):
            path_y_einz = os.path.join(path_p_einz,year,"Einzel")

            if count == 0:
                peri_einzel_list = [] + [path_y_einz]
                count += 1
            else:
                peri_einzel_list.append(path_y_einz)

print(peri_einzel_list)

for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

############################ check branch .../Frienisberg_1997_2007/Datum/specific_date/Summe ###################################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_p_einz = os.path.join(path_geb,GEB,"Datum")

        for year in os.listdir(path_p_einz):
            path_y_einz = os.path.join(path_p_einz,year,"Summe")

            if count == 0:
                peri_einzel_list = [] + [path_y_einz]
                count += 1
            else:
                peri_einzel_list.append(path_y_einz)

print(peri_einzel_list)

for dat_einzel in peri_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")








###################################### check branch . .../Frienisberg_1997_2007/Parzelle/specific field/Einzel #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_origin = os.path.join(path_geb,GEB,"Parzelle")
        for date in os.listdir(path_origin):
            date_path = os.path.join(path_origin,date,"Einzel")

            if count == 0:
                date_einzel_list = [] + [date_path]
                count += 1
            else:
                date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

###################################### check branch . .../Frienisberg_1997_2007/Erosionsform/linear/Einzel #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        date_path = os.path.join(path_geb, GEB, "Erosionsform","linear","Einzel")

        if count == 0:
            date_einzel_list = [] + [date_path]
            count += 1
        else:
            date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel, ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

###################################### check branch . .../Frienisberg_1997_2007/Erosionsform/flaechenhaft/Einzel #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        date_path = os.path.join(path_geb, GEB, "Erosionsform","flaechenhaft","Einzel")

        if count == 0:
            date_einzel_list = [] + [date_path]
            count += 1
        else:
            date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel, ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")


###################################### check branch . .../Frienisberg_1997_2007/Erosionsform/linear/Summe #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        date_path = os.path.join(path_geb, GEB, "Erosionsform","linear","Summe")

        if count == 0:
            date_einzel_list = [] + [date_path]
            count += 1
        else:
            date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel, ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")


###################################### check branch . .../Frienisberg_1997_2007/Erosionsform/flaechenhaft/Summe #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete, geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        date_path = os.path.join(path_geb, GEB, "Erosionsform","flaechenhaft","Summe")

        if count == 0:
            date_einzel_list = [] + [date_path]
            count += 1
        else:
            date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel, ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")


###################################### check branch . .../Frienisberg_1997_2007/Parzelle/specific field/Einzel #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_origin = os.path.join(path_geb,GEB,"Parzelle")
        for date in os.listdir(path_origin):
            date_path = os.path.join(path_origin,date,"Einzel")

            if count == 0:
                date_einzel_list = [] + [date_path]
                count += 1
            else:
                date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")


###################################### check branch . .../Frienisberg_1997_2007/Parzelle/specific field/Summe #####################
count = 0
for geb in os.listdir(Gebiete):
    path_geb = os.path.join(Gebiete,geb)
    os.chdir(path_geb)
    for GEB in os.listdir(path_geb):
        path_origin = os.path.join(path_geb,GEB,"Parzelle")
        for date in os.listdir(path_origin):
            date_path = os.path.join(path_origin,date,"Summe")

            if count == 0:
                date_einzel_list = [] + [date_path]
                count += 1
            else:
                date_einzel_list.append(date_path)

print(date_einzel_list)

for dat_einzel in date_einzel_list:
    arcpy.env.workspace = dat_einzel
    rasList = arcpy.ListRasters()

    for ras in rasList:
        check_path = os.path.join(dat_einzel,ras)

        if os.path.basename(check_path)[0:4] == "numpy":
            print(os.path.basename(check_path) + " will be deleted")
            arcpy.Delete_management(check_path)
        #else:
            #print(ras + " is no strange raster")

print("checking process has been successfully finished :)")

