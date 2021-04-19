


#n by 24 by 7 by (num_days), with a separate  
#the use of multiple labels averages models
function model_data_gen(n = 150,num_days = 10)
    ret = Array{Float32}(undef,24,7,num_days,1,n)
    real = Array{Float32}(undef,24,7,n)
    #splitting into 3D assumes datapoint relationships based on proximity
    #i think this is reasonable, as x-proximity is hour proximity,
    #and y-proximity is also similar based on time.
    #z-proximity is relevant if we assume that the days are in chronological order
    
    for i in 1:n
        #maybe in the future we do better proximity based bleed so the model works more effectively (would be more representative data?)
        #need proximity based bleed 
        #(assumed trends over time -> similarity based on close timescale)
        real[:,:,i] .= randn(24,7) 
        for j in 1:num_days
            #entangle across samples
            #each sample has some arbitrary change
            ret[:,:,j,1,i] .= real[i] .+ randn()
        end
    end
    ret .+= .25*randn(size(ret))
    ret .= (ret .- minimum(ret)) ./ maximum(ret)
    real .= (real .- minimum(real)) ./ maximum(real)
    return ret[:,:,:,:,1:52],real[:,:,1:52],ret[:,:,:,:,53:end]
end