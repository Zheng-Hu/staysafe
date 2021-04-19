using Flux: ADAM, gradient, glorot_uniform, conv, train!, Chain, params, mse
using Flux.Optimise: update!
#trains and utilizes a prediction model to output congestion metrics
function predict()


    train,valid,test = model_data_gen()
    #split into train and valid
    valid_form = reshape(valid,:,size(valid,3))

    #using 3D conv models because they're cool and seem relevant
    #performing learned calcs with bleed into other days of week
    cfilter1 = glorot_normal(3,3,3,1,9) #3645 params. maybe decrease channel size
    cfilter2 = glorot_normal(3,3,3,9,81) #consider decreasing channels
    conv1 = x -> conv(x,cfilter1,pad=1)
    conv2 = x -> conv(x,cfilter2,pad=1)
    

    #the output of the conv2 layer will be a 5D tensor, 24 x 7 x 10 x 9 x (num). We need to get that into something workable.
    res = x -> reshape(x,:,size(x,5))
    combine = Dense(136080,168)
    #@show size(res(conv2(conv1(train))))

    #
    model = Chain(conv1,x -> relu.(x),conv2,x -> relu.(x),
                    res,combine)

    #note that this model is more denoising than prediction...
    #i am effectively "denoising" a 24/7 set of data to get hopefully
    #accurate prediction. not sure if this is the right approach. 
    

    loss(noisy,clean) = mse(model(noisy),clean)
    #@show loss()

    for i in 1:20
        train!(loss,params(cfilter1,cfilter2,combine),[(train,valid_form)],ADAM(.0001))
        #grade the model on data after each iterations
        @show loss(train,valid_form)
    end
    #@show mean(test)
    #run on test and output
    return model(test)
end