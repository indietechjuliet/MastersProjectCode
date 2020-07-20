#This file converts one of the VCf relatedness files to an NxN matrix
#Note: these files are specifically from VCFtools --relatedness and 
#--relatedness2 options
#Date: July 18th 2020
#Author: Rachel Offutt

#parse through the gathered relatedness numbers and print an
#NxN matrix
def parseRelatednessandPrint(samples, outMatrix):
    
    #open the specified output files
    fout =  open(outMatrix, "w")
    samplesList = []
    fout.write(",")

    #print the header of samples
    for p_id, p_info in samples.items():
        samplesList.append(p_id)
        fout.write(p_id+",")

    fout.write("\n")

    #Since VCFtools is efficent and does not repeat comparisons,
    #I check for the compariosn in the order Sample X to Sample Y
    #as well as Sample Y to Sample X
    for i in range(0, len(samplesList)):
        fout.write(samplesList[i]+",")
        for j in range(0, len(samplesList)):
            if samplesList[i] in samples and samplesList[j] in samples[samplesList[i]]:
                fout.write(samples[samplesList[i]][samplesList[j]]+",")
            else:
                if samplesList[j] in samples and samplesList[i] in samples[samplesList[j]]:
                    fout.write(samples[samplesList[j]][samplesList[i]]+",")
                else:
                    fout.write("NOT FOUND"+",")
        fout.write("\n")

#This function reads in the relatedness and stores in a dictionary of 
#dictionaries
def getSamplesandRelatedness(inFile):
    
    fin = open(inFile, "r")
    samples = {}
    for num, line in enumerate(fin):
        line = line.split("\t")
        #print(line)
        if num > 1:
            relatedness = line[-1]
            if "\n" in relatedness:
                relatedness = relatedness[:-1]
            if line[0] not in samples:
                temp = {}
                temp[line[1]] = relatedness
                samples[line[0]] = temp
            else:
                samples[line[0]][line[1]] = relatedness

    return samples;


def main():
    #################USER EDITS THESE PATHS########################
    inFile = "min_vcftoolsrelatedness.relatedness"

    outMatrix = "min_vcftools_relatedness1.csv"
    
    ###############################################################

    samples = {}

    samples = getSamplesandRelatedness(inFile)
    
    parseRelatednessandPrint(samples, outMatrix)



if __name__ == "__main__":
    main()

