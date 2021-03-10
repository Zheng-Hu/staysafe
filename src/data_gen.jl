using CSV
using DataFrames
using Distributions
using Random

days = Dict([
    (0,"Sunday"),
    (1,"Monday"),
    (2,"Tuesday"),
    (3,"Wednesday"),
    (4,"Thursday"),
    (5,"Friday"),
    (6,"Saturday"),
])

n = 100
f = open("building_names.txt")
s = readlines(f)

buildings = Array{Any}(missing,n,4)
congestion = Array{Any}(missing,24*7*n,4)

building_labels = ["id","building_name","longitude","latitude"]
congestion_labels = ["owner_id","day_of_week", "time_period", "cong_level"]
#number of people we're generating
for i in 1:n
    first = (i-1)*24*7
    #TODO: better name initialization
    
    buildings[i,1] = i #ID
    buildings[i,2] = s[i] #NAME
    #centered on ann arbor for easier plotting
    buildings[i,3] = 42.2808 + .1 * (rand() - .5) #LONG
    buildings[i,4] = 83.7430 + .1 * (rand() - .5) #LAT

    congestion[first+1:first+24*7,1] .= i

    for j in 0:6
        local d = Normal(0,1 + 2*rand()) #random standard deviation, 1-3
        local lo,hi = -2,2 #standard deviations out
        local x = range(lo,hi;length=24)
        congestion[first+24*j+1:first+24*j+24,2] .= j
        congestion[first+24*j+1:first+24*j+24,3] = Array(1:24)
        congestion[first+24*j+1:first+24*j+24,4] = pdf.(d,x) * (.75+.5 * rand()) / mean(pdf.(d,x)) #up to double the dist
    end
end

for j in 0:6
    autolabels[24*j+1:24*j+24] = string.(days[j],string.(1:24))
end

#generate the label scheme
labels = ["Name","ID","Longitude","Latitude"]
labels = cat(labels,autolabels,dims=1)

df = DataFrame(buildings,building_labels)
CSV.write("buildings.csv", df)

df2 = DataFrame(congestion,congestion_labels)
CSV.write("congestion.csv", df2)


#basically, each day has a "person quantity"
#which is spread via a normal distribution.
#standard congestion at a data point is 1.
#average congestion per day varies from .75 to 1.25.
#might wanna add more customization if you want?
"""
plot()
plot(title = "Monday at 01",data[1,5:28],yrange=[.5,1.5],label = "Monday at Building#1",xlabel = "Hour",ylabel = "Congestion")
#plot!(title = "Tuesday at 01",data[1,29:52],yrange=[.5,1.5],label="Tuesday at Building#1")
plot!(title = "Monday at 02",data[2,5:28],yrange=[.5,1.5],label = "Monday at Building#2")
plot!(title = "Congestion Data Sample",data[1,29:52],yrange=[.5,1.5],label = "Tuesday at Building#2")
"""