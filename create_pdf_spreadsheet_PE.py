#script that makes for each region-period object, like Frienisberg 1997-2007, an overview spreadsheet

import os
import xlrd
import arcpy
from arcpy.sa import *
import numpy as np
arcpy.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
import matplotlib as mpl
import matplotlib.pyplot as plt
import statistics as stat
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Image
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter


#input path (begin of the tree-folder-structure)
Gebiete = r"E:\David_Remund_Masterarbeit\alle_GE_MA\Gewässereintrag"

#definition to round e.g. 12 to 10, 13 to 15, 18 to 20,...
def myround5(x, base=5):
    return base * round(x/base)

#definition to round e.g. 1.5 to 2, 1.2 to 1,...
def myround1(x, base=1):
    return base * round(x/base)

#round to next 0.25 float
def myround_25(x, base=0.25):
    return base * round(x/base)

from datetime import date
def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).
    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

#for the sediment input, make a list of region-period paths,e.g. ...\Frienisberg_1997_2007
count = 0
SE_path = os.path.join(Gebiete,"Phosphoreintrag")

for Geb in os.listdir(SE_path):
    geb_path = os.path.join(SE_path,Geb)

    for geb_peri in os.listdir(geb_path):
        geb_peri_path = os.path.join(geb_path, geb_peri)

        if count == 0:
            geb_peri_list = [] + [geb_peri_path]
            count += 1
        else:
            geb_peri_list.append(geb_peri_path)

print(geb_peri_list)

################## for each region-period object, like Frienisberg 1997-2007, make a spreadsheet that includes
################## the total sediment input [t], the mean annual sediment input [t/ha*a], boxplots and timeseries

for GEB_PERI in geb_peri_list:
    ############ for each sediment input raster in e.g. Frienisberg 97-07,
    ############ calculate it's sum [t] and at the sum-value to a list

    # extract title string e.g. "Frienisberg 1997-2007" -> used later in spreadsheet
    title_string = GEB_PERI.split(os.sep)[6]
    title_string = "overview phosphor input " + title_string.partition('_')[0] + " " + (title_string.partition('_')[2])[:-5] + "-" + (title_string.partition('_')[2])[-4:]
    print(title_string)


    #go to the folder with all sediment input rasters in e.g. Frienisberg 1997-2007
    peri_einzel_path = os.path.join(GEB_PERI,"Periode","Einzel")
    arcpy.env.workspace = peri_einzel_path
    SE_list = arcpy.ListRasters()

    count = 0
    for ras in SE_list:
        # make a Raster
        inRas = arcpy.Raster(os.path.join(peri_einzel_path, str(ras)))

        # Convert Raster to numpy array
        arr = arcpy.RasterToNumPyArray(inRas)
        arr = arr.astype(float)
        arr[arr == 0] = np.nan

        sum_notNAN = np.count_nonzero(~np.isnan(arr))  # ~ inverts the boolean matrix returned from np.isnan
        area_ha = sum_notNAN * 4 / 10000

        arr_mean = np.nanmean(arr)  # wenn man nan-Werte hat, dann mit np.nanmean(arr) arbeiten...

        # mean in [t/ha]  und area_ha die Fläche in [ha] -> t/ha * ha = sediment input [t] (-> Eintrag_t)
        Eintrag_t = arr_mean * area_ha

        if count == 0:
            Tonnen_Eintrag = [] + [Eintrag_t]
            count += 1
        else:
            Tonnen_Eintrag.append(Eintrag_t)

    # total sum of the region-period object [t]
    sum_Tonnen_Eintrag = sum(Tonnen_Eintrag)
    print(sum(Tonnen_Eintrag))  # for control purposes

    #rename Tonnen_Eintrag list
    data = Tonnen_Eintrag

    ########## calculate for the Tonnen_Eintrag list some statistics #############

    # calculate mean, SD, max, min
    mean = round(stat.mean(Tonnen_Eintrag), 2)  # for the mean-list
    Mittel = "mean: " + str(round(stat.mean(Tonnen_Eintrag), 2))
    SD = str(round(stat.stdev(Tonnen_Eintrag), 2))
    Max = "max: " + str(round(max(Tonnen_Eintrag), 2))
    Min = "min: " + str(round(min(Tonnen_Eintrag), 2))

    # convert the Tonnen_Eintrag list to a numpy array and calculate percentiles
    Tonnen_np = np.array(Tonnen_Eintrag)
    perc_25 = "perc25: " + str(round(np.percentile(Tonnen_np, 25), 2))
    perc_50 = "perc50: " + str(round(np.percentile(Tonnen_np, 50), 2))
    perc_75 = "perc75: " + str(round(np.percentile(Tonnen_np, 75), 2))
    p25 = np.percentile(Tonnen_np, 25) #use p25 and p50 to set y_lim in the boxplot
    p75 = np.percentile(Tonnen_np, 75)


    # get the name of the region-period, e.g Frienisberg97 for Frienisberg 1997-2007 // also add some statistics as strings
    re_pe = GEB_PERI.split(os.sep)[6]
    re_pe = re_pe.partition('_')[0] + re_pe[-2:]
    re_pe_name = "\n" + Mittel + "±" + SD + "\n" + "\n" + Min + "\n" + perc_25 + "\n" + perc_50 + "\n" + perc_75 + "\n" + Max
    # re_pe.partition('_')[0] + re_pe_name[-2:]+ "\n" + -> add this, if you have more sub-boxplots...
    print(re_pe_name)

    #### calculate mean annual input [kg/ha*a]

    # length period is different form 97-07 and 07-17
    if re_pe[-2:] == "07":
        lenght_period = 9.52
    if re_pe[-2:] == "17":
        lenght_period = 9.41

    print("length period: " + str(lenght_period))

    # different regions have different ha-size
    if re_pe[:-2] == "Frienisberg":
        area_ha = 57.483
    if re_pe[:-2] == "Lobsigen":
        area_ha = 55.468
    if re_pe[:-2] == "Schwanden":
        area_ha = 37.208
    if re_pe[:-2] == "Seedorf":
        area_ha = 15.931
    if re_pe[:-2] == "Suberg":
        area_ha = 99.325

    print("area_ha: " + str(area_ha))

    # calculate mean in t/ha*a --> this is the mean annual input over the whole region in the wohle period
    mean_input = sum_Tonnen_Eintrag / (lenght_period * area_ha)
    print("mean input: " + str(mean_input))

    #make the labels-list for later...
    labels = [] + [re_pe_name]

    #do this to plot the mean later...
    # add the [mean-value] of e.g. Frienisberg07-17 to the list "mean_list"
    #corr_shift_plot_value = [0]
    #mean_list = [corr_shift_plot_value] + [mean]

    # data list
    print(data)
    # labels list
    print(labels)

    ################# make the boxplots
    fig = plt.figure(figsize=(4, 6))
    # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot
    bp = ax.boxplot(data,showmeans=True, meanprops = {"marker" :'o', "markeredgecolor" :'green',
                          "markerfacecolor":'green', "markersize":3}) #don't use dict as built-in variable (lik on websites...)

    #set y lim
    upper_whisker = (p75+((p75-p25)*1.5))
    # set y axis min and max
    ax.set_ylim(0.0, myround_25(upper_whisker)+0.25)

    # set x and y axis
    plt.xticks(np.arange(len(labels)) + 1, labels, fontsize=10)
    plt.yticks(np.arange(0.0,myround_25(upper_whisker)+0.25, step=0.25), fontsize=14)
    ax.set_ylabel('phosphor input [kg]', fontsize=18)

    #plt.title(re_pe, fontsize=20)

    # add a y-grid to the boxplot
    plt.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.25)

    ## change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set(color='#7570b3', linewidth=1)

    ## change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=1)

    ## change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=1)

    ## change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color="r", linewidth=1)  # https://matplotlib.org/examples/color/named_colors.html

    ## change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='', color='#e7298a', alpha=2,
                  markersize=0.8)  # alpha is kind of dot transparency #marker = '', because single dots should not be plotted...

    # save the boxplots as e.g. Frienisberg07_bp.png => this folder had to be created new!
    save_path = r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\boxplots_PE"
    # Save the figure
    fig.savefig(os.path.join(save_path, re_pe + '_bp.png'), bbox_inches='tight')

    #########################################################################################
    ###################### do the timeseries ################################################

    geb_peri_datum = os.path.join(GEB_PERI,"Datum")
    # get a list of e.g....Frienisberg_1997_2007/Datum/Summe paths
    cnt = 0
    for dat in os.listdir(geb_peri_datum):
        dat_path = os.path.join(geb_peri_datum, dat, "Summe")

        if cnt == 0:
            datpath_list = [] + [dat_path]
            cnt += 1
        else:
            datpath_list.append(dat_path)

    print(datpath_list)

    COUNT = 0
    CNT = 0
    for Dat in datpath_list:
        ############### extract the date and format it new
        date = Dat.split(os.sep)[8]
        date = date.replace("_", "-")
        # datetime conversion
        date = datetime.strptime(date, '%Y-%m-%d')
        print(date)

        # add date to a new list that records all dates of e.g. Frienisberg_97_07
        if COUNT == 0:
            date_list = [] + [date]
            COUNT += 1
        else:
            date_list.append(date)

        ####################calculate the date_sum and add it to dateSUM list
        arcpy.env.workspace = Dat
        # consists only of sum_raster of a certain date
        DAT_list = arcpy.ListRasters()

        # for a certain date in e.g. Frienisberg_97_07,e.g. 1998_09_16, calculate the sum of the sediment input [t]
        for ras in DAT_list:
            # make a Raster
            inRas = arcpy.Raster(os.path.join(Dat, str(ras)))

            # Convert Raster to numpy array
            arr = arcpy.RasterToNumPyArray(inRas)
            arr = arr.astype(float)
            arr[arr == 0] = np.nan

            sum_notNAN = np.count_nonzero(~np.isnan(arr))  # ~ inverts the boolean matrix returned from np.isnan
            area_ha = sum_notNAN * 4 / 10000

            arr_mean = np.nanmean(arr)  # wenn man nan-Werte hat, dann mit np.nanmean(arr) arbeiten...

            # mean in [t/ha]  und area_ha die Fläche in [ha] -> t/ha * ha = sediment input [t] (-> Eintrag_t)
            sum_Eintrag = arr_mean * area_ha
            print(sum_Eintrag)

            # add sum_Eintrag to a new list that records the total sum of a the dates,e.g. sum 1998_09_16, then sum 1998_11_06,...
            if CNT == 0:
                dateSUM_list = [] + [sum_Eintrag]
                CNT += 1
            else:
                dateSUM_list.append(sum_Eintrag)

    print(dateSUM_list)
    print(sum(dateSUM_list))
    print(date_list)

    max_SE = max(dateSUM_list)

    # make a pandas dataframe
    dict = {"Sum_SE": dateSUM_list, "date": date_list}
    print(dict)
    df = pd.DataFrame(dict)
    df

    # create the plot space upon which to plot the data
    fig, ax = plt.subplots(figsize=(10, 10))

    # add the x-axis and the y-axis to the plot
    ax.plot(df['date'],
            df['Sum_SE'],
            color='red',linewidth=0.5)

    if int(re_pe[-2:]) == 7:
        # set x axis min and maxdate
        min_date = datetime.strptime("1998-01-01", '%Y-%m-%d')
        max_date = datetime.strptime("2008-01-01", '%Y-%m-%d')
        plt.xticks(np.array(['1998-01-01T00:00:00.000000', '1999-01-01T00:00:00.000000',
           '2000-01-01T00:00:00.000000', '2001-01-01T00:00:00.000000',
           '2002-01-01T00:00:00.000000', '2003-01-01T00:00:00.000000',
           '2004-01-01T00:00:00.000000', '2005-01-01T00:00:00.000000',
           '2006-01-01T00:00:00.000000', '2007-01-01T00:00:00.000000',
           '2008-01-01T00:00:00.000000']),fontsize = 14)
    if int(re_pe[-2:])== 17:
        #set x axis min and maxdate
        min_date = datetime.strptime("2008-01-01", '%Y-%m-%d')
        max_date = datetime.strptime("2018-01-01", '%Y-%m-%d')
        plt.xticks(np.array(['2008-01-01T00:00:00.000000', '2009-01-01T00:00:00.000000',
                             '2010-01-01T00:00:00.000000', '2011-01-01T00:00:00.000000',
                             '2012-01-01T00:00:00.000000', '2013-01-01T00:00:00.000000',
                             '2014-01-01T00:00:00.000000', '2015-01-01T00:00:00.000000',
                             '2016-01-01T00:00:00.000000', '2017-01-01T00:00:00.000000',
                             '2018-01-01T00:00:00.000000']), fontsize=14)

    #diff_date = datetime.strptime("1999-01-01", '%Y-%m-%d') - datetime.strptime("1998-01-01", '%Y-%m-%d')
    # plt.xticks(np.arange(min_date, max_date, step= diff_date), fontsize=14)#stimmt nicht genau, da Schaltjahre nicht berücksichtigt werden...
    # auf diese Art sind die Ticks sowieso falsch, da ein Jahr verschoben gelabelt wird...ging es auch einfacher als array fix definieren..

    ax.set_xlim(min_date, max_date)

    #rotate tick labels
    plt.setp(ax.get_xticklabels(), rotation=90)

    # fontsize y-labes
    plt.ylabel('Phosphor input [kg]', fontsize=18)

    #different scale depending on the max_SE
    if max_SE < 10:
        ax.set_ylim(0.0, myround1(max_SE) + 1)
        plt.yticks(np.arange(0.0, myround1(max_SE)+1, step=0.5), fontsize=14)

    else:
        # set y axis min and max
        ax.set_ylim(0.0, myround5(max_SE) + 5)
        plt.yticks(np.arange(0.0, myround5(max_SE) + 5, step=5), fontsize=14)

    # add a y-grid
    plt.grid(axis="y", color='lightgray', linestyle='-', linewidth=0.25)

    # --> this folder had to be created new!
    SAVE_path = r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\timeseries_PE"
    # Save the figure
    fig.savefig(os.path.join(SAVE_path, re_pe + '_ts.png'))
    # -> the spreadsheets_PE folder had to be created new!
    c = canvas.Canvas(
        os.path.join(r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\spreadsheets_PE",re_pe+ "_PE_spreadsheet.pdf"),
        pagesize=letter)
    width, height = letter  # so kann man auf die Weite und Höhe zugreifen!
    c.setFont('Helvetica-Bold', 20)  # only helvetica is not bold...

    #draw the title of the pdf
    c.drawCentredString(width / 2, height - 1.2 * cm, title_string)

    # set new font
    c.setFont('Helvetica', 12)
    # draw the total and mean annual input
    c.drawCentredString(width / 2, height - 2.4 * cm,
                        "sum of toal phosphorus input: " + str(round(sum_Tonnen_Eintrag, 2)) + " kg")
    c.drawCentredString(width / 2, height - 3.6 * cm,
                        "mean annual phosphorus input: " + str(round(mean_input, 2)) + " kg/ha*a")

    #draw the timeseries -> folder path had to be adapted
    c.drawImage(os.path.join(r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\timeseries_PE",re_pe+"_ts.png"),
        width / 2 - 6 * cm, 0.0 * cm, width=12 * cm, height=12 * cm,
        preserveAspectRatio=True)  # wenn das Bild 12cm weit ist, dann bei width/2-6cm beginnen, um zu zentrieren

    #draw the boxplot -> folder path had to be adapted
    c.drawImage(os.path.join(r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\boxplots_PE",re_pe+"_bp.png"),
        width / 2 - 6 * cm, height - 17 * cm, width=12 * cm, height=12 * cm, preserveAspectRatio=True)

    c.save()

# merge all the pdf-pages into one document -> folder path had to be adapted
spreadsheet_folder = r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\spreadsheets_PE"

#make a list of spreadsheet paths
CT = 0
for spr_sheet in os.listdir(spreadsheet_folder):
    spr_path = os.path.join(spreadsheet_folder,spr_sheet)

    if CT == 0:
        spr_path_list = [] + [spr_path]
        CT += 1
    else:
        spr_path_list.append(spr_path)
print(spr_path_list)


from PyPDF2 import PdfFileMerger, PdfFileReader

merger = PdfFileMerger()
for filename in spr_path_list:
    merger.append(PdfFileReader(filename)) #file(filename, 'rb')

# the destination folder had to be adapted...(always the name had to be changed from SE to PE)
# unit had to be changed from t to kg...
destination_folder = r"E:\David_Remund_Masterarbeit\alle_GE_MA\scripts_for_GE\geodata_analysis\figures_spreadsheet\overview_phosphor_input"
merger.write(os.path.join(destination_folder,"phosphor_input_overview.pdf"))
