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
data = Array{Any}(missing,n,4+24*7)
autolabels = Array{String}(undef,24*7)
#number of people we're generating
for i in 1:n
    
    #TODO: better name initialization
    
    data[i,1] = randstring(rand(4:8))




    data[i,2] = i
    #centered on ann arbor for easier plotting
    data[i,3] = 42.2808 + .1 * (rand() - .5)
    data[i,4] = 83.7430 + .1 * (rand() - .5)

    for j in 0:6
        local d = Normal(0,1 + 2*rand()) #random standard deviation, 1-3
        local lo,hi = -2,2 #standard deviations out
        local x = range(lo,hi;length=24)
        data[i,24*j+5:24*j+28] = pdf.(d,x) * (.75+.5 * rand()) / mean(pdf.(d,x)) #up to double the dist
    end
end

for j in 0:6
    autolabels[24*j+1:24*j+24] = string.(days[j],string.(1:24))
end

#generate the label scheme
labels = ["Name","ID","Longitude","Latitude"]
labels = cat(labels,autolabels,dims=1)

df = DataFrame(data,labels)
CSV.write("sample_data.csv", df)

#basically, each day has a "person quantity"
#which is spread via a normal distribution.
#standard congestion at a data point is 1.
#average congestion per day varies from .75 to 1.25.
#might wanna add more customization if you want?
plot()
plot(title = "Monday at 01",data[1,5:28],yrange=[.5,1.5],label = "Monday at 01",xlabel = "Hour",ylabel = "Congestion")
plot!(title = "Tuesday at 01",data[1,29:52],yrange=[.5,1.5])
plot!(title = "Monday at 02",data[2,5:28],yrange=[.5,1.5],label = "Monday at 02")
plot!(title = "Data",data[1,29:52],yrange=[.5,1.5],label = "Tuesday at 02")
