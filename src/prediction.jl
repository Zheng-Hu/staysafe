using Flux: ADAM, gradient, glorot_uniform, conv, train!, Chain, params, mse
using Flux.Optimise: update!
#trains and utilizes a prediction model to output congestion metrics
function predict()


    data,real = model_data_gen()
    #split into train and valid


    #using 3D conv models because they're cool and seem relevant
    #performing learned calcs with bleed into other days of week
    cfilter1 = glorot_normal(3,3,3,1,9) #3645 params. maybe decrease channel size
    cfilter2 = glorot_normal(3,3,3,9,81) #consider decreasing channels
    conv1 = x -> conv(x,cfilter1,pad=1)
    conv2 = x -> conv(x,cfilter2,pad=1)
    
    #the output of the conv2 layer will be a 5D tensor, 24 x 7 x (num days) x 1 x 81. We need to get that into something workable.
    #and we need to simplify numdays x 81 to a single congestion metric.
    #todo: combine
    combine = glorot_normal(64,16)


    #
    model = Chain(conv1,x -> relu.(x),conv2,x -> relu.(x),
                    x -> mapslices(y -> fc1 * y,x,dims=[3]))

    #note that this model is more denoising than prediction...
    #i am effectively "denoising" a 24/7 set of data to get hopefully
    #accurate prediction. not sure if this is the right approach. 
    

    loss = 

    for i in 1:niters
        #train the model on our data
    end


    #grade the model on data after each iterations


    #TODO: run on test and output

end