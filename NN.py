import numpy as np
import random
np.random.seed(0)

class Layer_Dense:
    def __init__(self,n_input,neurons):
        self.test = random.randint(3,7)
        self.weight = np.random.rand(n_input,neurons)
        self.biases = np.ones((1,neurons))
        self.weight_bias = np.random.rand(1,neurons)
    def forward(self,inputs):
        self.output = (np.dot(inputs,self.weight) + self.biases*self.weight_bias)



class NeuralNetWork:
    def __init__(self,n_input,n_output,n_layer,node_hidden):
        self.X = n_input
        self.Y = n_input
        self.denes_layers = []
        if n_layer == 0:
            node_hidden = 0
            self.denes_layers.append(Layer_Dense(n_input,n_output))
        else:
            for ilayer in range(n_layer+1):
                if ilayer == 0:
                    self.denes_layers.append(Layer_Dense(n_input,node_hidden))
                elif (ilayer == n_layer) :
                    self.denes_layers.append(Layer_Dense(node_hidden,n_output))
                else:
                    self.denes_layers.append(Layer_Dense(node_hidden,node_hidden))
 
    def sigmoidActivation(self,output):
        return 1 / ( 1 + np.exp(-output))

    def ReLUActivation(self,output):
        for iOutput in range(len(output)):
            output[iOutput] = max(0,output[iOutput])
        return output
    
    def tanhActivation(self,output):
        return np.tanh(output)

    def forwardPropagation(self,inputs):
        self.output = []
        for layer in self.denes_layers:
            if layer == self.denes_layers[0]:
                layer.forward(inputs)
            else:
                layer.forward(self.output)
            self.output = self.sigmoidActivation(layer.output)

    def constructFromSameDenses(self,outside_denes_layers):
        self.denes_layers = outside_denes_layers
    
    def weightMutation(self,rate):
        for layer in self.denes_layers:
            for irow in range(len(layer.weight)): 
                for icol in range(len(layer.weight[irow])):
                    if random.random() < rate:
                        layer.weight[irow][icol] =  layer.weight[irow][icol] + np.random.normal(0, 0.1)
            
            for irow in range(len(layer.weight_bias)): 
                for icol in range(len(layer.weight_bias[irow])):
                    if random.random() < rate:
                        layer.weight_bias[irow][icol] =  layer.weight_bias[irow][icol] + np.random.normal(0, 0.1)    
        
    def GenerateIndexColMutate(self,rate,layer):
        Nrol = layer.weight.shape[1]
        iMutateColWieght = []
        for icol in range(Nrol):
            if random.random() < rate:
                iMutateColWieght.append(icol)

        Nrol = layer.weight_bias.shape[1]
        iMutateColBias = []
        for icol in range(Nrol):
            if random.random() < rate:
                iMutateColBias.append(icol)
        
        return iMutateColWieght, iMutateColBias
                
    def SwapColNN(self,iMutateCol,ilayer,newNN,typeMatrix):
        layer = self.denes_layers[ilayer]
        if typeMatrix == "W":
            for irow in range(len(layer.weight)):
                for icol in iMutateCol:
                    val = layer.weight[irow][icol]
                    layer.weight[irow][icol] = newNN.denes_layers[ilayer].weight[irow][icol]
                    newNN.denes_layers[ilayer].weight[irow][icol] = val
        
        if typeMatrix == "B":
            for irow in range(len(layer.weight_bias)):
                for icol in iMutateCol:
                    val = layer.weight_bias[irow][icol]
                    layer.weight_bias[irow][icol] = newNN.denes_layers[ilayer].weight_bias[irow][icol]
                    newNN.denes_layers[ilayer].weight_bias[irow][icol] = val

    def crossOverNN(self,rate,newNN):
        for ilayer in range(len(self.denes_layers)):
            iMutateColWieght, iMutateColBias = self.GenerateIndexColMutate(rate,self.denes_layers[ilayer])
            self.SwapColNN(iMutateColWieght,ilayer,newNN,"W")
            self.SwapColNN(iMutateColBias,ilayer,newNN,"B")



            





