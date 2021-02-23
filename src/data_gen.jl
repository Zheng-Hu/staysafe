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
data = Array{Any}(missing,n,4+96*7)
autolabels = Array{String}(undef,96*7)
#number of people we're generating
for i in 1:n
    data[i,1] = randstring(rand(4:8))
    data[i,2] = i
    #centered on ann arbor for easier plotting
    data[i,3] = 42.2808 + .1 * (rand() - .5)
    data[i,4] = 83.7430 + .1 * (rand() - .5)

    for j in 0:6
        local d = Normal(0,1 + 2*rand())
        local lo,hi = -2,2
        local x = range(lo,hi;length=96)
        data[i,96*j+5:96*j+100] = pdf.(d,x) * (.75+.5 * rand()) / mean(pdf.(d,x)) #up to double the dist
    end
end
for j in 0:6
    autolabels[96*j+1:96*j+96] = string.(days[j],string.(1:96))
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
