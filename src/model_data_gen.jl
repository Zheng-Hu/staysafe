


#n by 24 by 7 by (num_days), with a separate  
#the use of multiple labels averages models
function model_data_gen(n = 100,num_days = 10)
    ret = Array{Array{Float32}}(undef,n)
    real = Array{Array{Float32}}(undef,n)
    #splitting into 3D assumes datapoint relationships based on proximity
    #i think this is reasonable, as x-proximity is hour proximity,
    #and y-proximity is also similar based on time.
    #z-proximity is relevant if we assume that the days are in chronological order
    
    for i in 1:n
        reti = Array{Float32}(24,7,num_days)
        reali = Array{Float32}(24,7)
        #TOOO: entangle across days and hrs in starting init
        #need proximity based bleed 
        #(assumed trends over time -> similarity based on close timescale)
        reali = randn(24,7) 
        for j in 1:num_days
            #entangle across samples
            #each sample has some arbitrary change
            #TODO: proximity based!!
            reti[:,:,j] = reali .+ randn()
        end
        #add small noise
        reti .+= .25*randn(size(reti))
        #make all the congestions between 0 and 1
        reti .= exp.(reti .- maximum(reti))
        #set
        ret[i] = reti
        real[i] = reali
    end
    return ret,real
end