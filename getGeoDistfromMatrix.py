#Date: July 16th 2020
#Description: This script genertates an NxN matrix
#of geographic distances given a matrix with a header 
#of either sample ID's or sites. Note: Do not use Neighborhood
#as there is no way to go from Neighborood -> specific site
#To Run: python3 getGeoDistfromMatrix.py

import os
import sys
import math
# Python 3 program to calculate Distance Between Two Points on Earth 
from math import radians, cos, sin, asin, sqrt





def distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula  
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371

    # calculate the result 
    return(c * r)



#This matrix takes the list of sites, the path to the coordinatees file,
#and the name of the file you wish to write the distance matrix to. 
#Optionally, if you are wanting a sample-to-sample geographic distance,
#the optional argument sampleSames will be used and populated in main
def getMatrix(sitesList, coordinates, outFile, sampleNames = None):
    
    fout = open(outFile, "w")
    
    #Create the header for the matrix 
    for i in range(0, len(sitesList)):
        if i == 0:
            fout.write(",")

        if len(sampleNames) == 0:
            fout.write(sitesList[i]+",")
        else:
            fout.write(sampleNames[i]+",")

    fout.write("\n")

    #looping through all sites to make a square matrix, so nested loop
    for i in range(0, len(sitesList)):
        
        #outputting row header
        if len(sampleNames) != 0:
            fout.write(sampleNames[i]+",")
        else:
            fout.write(sitesList[i]+",")
        for j in range(0, len(sitesList)):
            
            lat1 = ""
            lat2 = ""
            lon1 = ""
            lon2 = ""
            fin = open(coordinates,"r")
            

            #getting the latitude and longitdes
            #NOTE: this is assuming your longitude is listed first, then latitude
            for num,line in enumerate(fin):
                if lat1 != "" and lat2 != "":
                    break;
                line = line.split(",")
                if line[0] == sitesList[i]:
                    lon1 = line[1]
                    lat1 = line[2]
                if line[0] == sitesList[j]:
                    lon2 = line[1]
                    lat2 = line[2]

            #Calling the distance formula and writing to outFile
            fout.write(str(float(distance(float(lat1), float(lat2), float(lon1), float(lon2))*1000))+",")
        fout.write("\n")
    fout.close()


#This function will only execute if you have provided
#a matrix of sample and need to get what site they belong 
#to
def convertSamplesToSites(samples, metadataFile):
    
    sites = []
    coutn = 0
    seen = []
    for i in range(0, len(samples)):
        found = 0
        coutn += 1
        fin = open(metadataFile, "r")
        for num, line in enumerate(fin):
            line = line.split(",")
            if line[0] == samples[i]:
                found = 1
                if samples[i] not in seen:
                    sites.append(line[2])
                    seen.append(samples[i])
                print("APPENDING  "+line[2] + " FOR   "+samples[i])
                continue;
        if found == 0:
            print("SAMPLE NOT FOUND - :"+samples[i])

    fin.close()
    print("COUNT   "+str(coutn))
    return sites;

#This function opens the matrix you specified as the inMatrix,
#and grabs the header of sites or samples. It also removes empty cells or 
#newline characters
def getHeaderInfo(inMatrix):

    fin = open(inMatrix, "r")
    header  = []
    tempHeader = []
    for num, line in enumerate(fin):
        if num < 1:
            tempHeader = line.split(",")
            break;
    fin.close()

    #checking for oddities
    for i in range(0, len(tempHeader)):
        if "" == tempHeader[i]:
            continue;
        else:
            if "\n" in tempHeader[i]:
                temp = tempHeader[i]
                temp = temp[:-1]
                tempHeader[i] = temp
            header.append(tempHeader[i])

    return header;


def main():

    ############################USER MUST MODIFY#######################################
    
    #specify the matrix whose header you want to get the geoegraphic distances for
    inMatrix = "/home/indietechjuliet/Desktop/min_variants_pwise.csv"

    #if the headers are expected to be samples, set to be true
    isSample = 1

    #path to site coordinates file
    coordinates = "sitecoordinates.csv"

    #path to file contaaing sample metadata, only relevant if samples and not sites are provided
    #Leave as empty string if not needed
    metadataFile = "minimalfilt_allGroups.v4.csv"
    
    #specify the name of the distance matrix you wish to output
    outFile = "minfilt_geoDist_v33.csv"

    ###################################################################################

    sitesList = []

    sitesList = getHeaderInfo(inMatrix)
    print(sitesList)
    print(len(sitesList))
    
    #if your matrix is sample-to-sample and not site-to-site, convert samples
    #to the sites they came from
    if isSample:
        samples = sitesList
        sitesList = convertSamplesToSites(sitesList, metadataFile)
        print(sitesList)
        print(len(sitesList))
    
    #take the sites, get their coordinates, and compute the distance between them, 
    #writes to outFile
    if isSample:
        getMatrix(sitesList, coordinates, outFile, sampleNames = samples)
    else:
        getMatrix(sitesList, coordinates, outFile)
    
    

    return 0;
    

if __name__ == "__main__":
    main()








