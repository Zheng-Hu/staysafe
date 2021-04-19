using CSV
using DataFrames
using Distributions
using Random

#generate multiple data points
#generate building categories

#number of buildings we're generating
n = 98
#building names file. we could randomize these if necessary
f = open("building_names.txt")
#read lines into an array of strings
s = readlines(f)
f2 = open("building_categories.txt")
s2 = readlines(f2)
#the end result is a bunch of CSV files in the format dictated by
#sample_data.sql
#for posterity:

building_labels = ["id","building_name","longitude","latitude","category"]
buildings = Array{Any}(missing,n,5)
congestion_labels = ["owner_id","day_of_week", "time_period", "cong_level"]
#less efficient since the markers are part of the data
#but my understanding is that this is easier to pull
#we could swap to n by 24*7 later potentially
congestion = Array{Any}(missing,24*7*n,4)

predicted_data = predict()
predicted_data = (predicted_data .- minimum(predicted_data))
predicted_data ./= maximum(predicted_data)

congestion[:,4] .= predicted_data[:]

#number of people we're generating
for i in 1:n
    #the first index in the congestion array (for this person)
    first = (i-1)*24*7
    
    buildings[i,1] = i #ID
    buildings[i,2] = s[i] #NAME
    #centered on ann arbor for plotting functionality
    buildings[i,3] = 42.2808 + .1 * (rand() - .5) #LONG
    buildings[i,4] = 83.7430 + .1 * (rand() - .5) #LAT
    buildings[i,5] = s2[i] #CATEGORY
    
    congestion[first+1:first+24*7,1] .= i

    for j in 0:6
        local d = Normal(0,1 + 2*rand()) #random standard deviation, 1-3
        local lo,hi = -2,2 #standard deviations out
        local x = range(lo,hi;length=24) #make a range to shove the pdf onto
        congestion[first+24*j+1:first+24*j+24,2] .= j
        congestion[first+24*j+1:first+24*j+24,3] = Array(1:24) 
        #create the normal dist. all of them are min 0 max 1
        #with different shapes potentially
        #congestion[first+24*j+1:first+24*j+24,4] = (pdf.(d,x) * (.75+.5 * rand()) / mean(pdf.(d,x)).-0.1754461039615053)/2 #0 to 1

    end
end



df = DataFrame(buildings,building_labels)
CSV.write("buildings.csv", df)

df2 = DataFrame(congestion,congestion_labels)
CSV.write("congestion.csv", df2)


#basically, each day has a "person quantity" from .75 to 1.25
#which is spread via normal distributions
#might wanna add more customization if you want?

#plot()
#plot(title = "Monday at 01",congestion[1:24,4],yrange=[0,1],label = "Monday at Building#1",xlabel = "Hour",ylabel = "Congestion")
#plot!(title = "Tuesday at 01",data[1,29:52],yrange=[.5,1.5],label="Tuesday at Building#1")
#plot!(title = "Congestion vs Time (testing)",congestion[25:48,4],yrange=[0,1],label = "Tuesday at Building#1")
