## ID: shahj29
## Number: 400252316


import pylab
import math 

##read the data and outputs the angles, intensity and peaks in a table provided
def getCoordinates (data):
    ##initializing lists for the lists  and initial values for counters 
    angles=[]
    intensity=[]
    peaks=[]
    count=0
    while count!=len (data):  #repeat the loop until every part of data is read
        if count%2==0:  #checks if count is even or odd, even means the value being read is an angle, odd means the value is an intensity
            angles.append((float(data[count])))  #convert the string to a float
        else:  
            if (data[count][-1][-1]=='*'):  #check if the value is a peak or not if it ends with a *
                peaks.append(int((count+1)/2))   #adds the exact element number at which the peak occurs to a list
            intensity.append(float(data[count].strip("*")))   #once the peak is dealt with, remove the * from the string and convert to a float
        count+=1  #increment the value by 1
    if len(intensity) == len(angles):
        return angles, intensity, peaks

        

##determines the width at the half way point of a maximum
def getBeta(data):
    betaVals= []  #initialize the empty list
    angle,intensity, peaks=(getCoordinates(data))   ##call the function to read the data and sets the lists returned to lists
    ## loop to determine the angles from the left and right of the maximum till the intensity is approximate to the half peak 
    for i in peaks:
        ##reset the initialized values at the beginning each time the loop iterates
        final=0
        initial=0
        bool= True
        half_peak= (intensity[i])/2  ##the half way point of the intensity 
        ##initialize a counter to i such that the loop will check each intensity value after the maximum occurs as long as its above or equal to the half-way point of the peak
        counter=i
        while bool==True :
            if (half_peak<=intensity[counter]):  ##check if the intensity is above or equal to the peak, add one if so
                counter+=1  
            else:
                final1= angle[counter-1]   ##record the value before the intensity is below the half-way point of the peak
                final2=angle[counter]      ##record the value after the intensity passes the half-way point
                final_approx1= abs(half_peak-final1)  ##figure out which one is closer
                final_approx2= abs(half_peak-final2)
                if final_approx1<final_approx2:   ##make final equal to the value closer to the half-way point
                    final=final1
                else:
                    final=final2
                bool=False       ##change the statement to false and exit the loop
                
        ##reset the variables and repeat the counter for before the peak occurs
        bool=True 
        counter=i 
        while bool==True :
            if (half_peak<=intensity[counter]):  ##check if the intensity is above or equal to the half way point
                counter-=1  
                
            else:
                initial= angle[counter+1]   ## if the intensity is above then record the value and exit the loop
                initial1= angle[counter-1]   ##record the value before the intensity is below the half-way point of the peak
                initial2=angle[counter]      ##record the value after the intensity passes the half-way point
                initial_approx1= abs(half_peak-initial1)
                initial_approx2= abs(half_peak-initial2)
                if initial_approx1<initial_approx2:     ##figure out which one is closer and make that one equal to the initial
                    initial=initial1
                else:
                    initial=initial2
                bool=False
        
        betaVals.append((final-initial))  ##the width is the final angle minus the initial  
    return betaVals ##return all the widths from each maximum

def XRD_Analysis (data):
    ##initializes the constants, empty lists, counters, calls the functions needed and assigns them to variables
    K=0.9
    lam= 0.07107
    nanoparticle=[]
    anglesMax=[]
    intensityMax=[]
    count=0
    angle,intensity, peaks=(getCoordinates(data))
    betaValues=getBeta(data)
    ##a loop to change every angle the max intensity occurs at and divids it by two (to get the theta from 2theta)
    for i in peaks:
        anglesMax.append(angle[i]/2) ##divide the 2theta angle by 2 
    ## a loop to determine the particle size for every peak occurance
    while count!=len(betaValues):  
        ##uses the Scherrer Equation, converts the width and angles to radians from degrees 
        particleSize=(K*lam)/(math.radians(betaValues[count])*math.cos(math.radians(anglesMax[count]))) 
        nanoparticle.append(particleSize) ##adds the values calculates to a list 
        count+=1
    average= (sum(nanoparticle)/len(nanoparticle)) ##calculates the average particle size by taking the sum and dividing by the number of elements in the list
    
    ##creates the graph and its axis by plotting the data using the intensity and angles lists created in the coordinates function
    pylab.title('XRD Intensity Plot', color = 'black', fontsize='12', horizontalalignment='center')
    pylab.ylabel('Intensity',  color = 'black', fontsize='12', verticalalignment='center')
    pylab.xlabel('2θ (deg)', color = 'black', fontsize='12', horizontalalignment='center')
    pylab.plot(angle,intensity)
    pylab.show()
    
    return (average) ##returns the average particle size 



##read the file with the table
input_file=open ("XRD_example1.txt","r")
contents = input_file.read().split()   ##split the file to make it a list 
input_file.close()

##call the functions needed to test the program

##getCoordinates(contents)
##getBeta(contents)
XRD_Analysis(contents)
