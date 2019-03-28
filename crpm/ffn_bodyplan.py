"""General feed forward network body plan.
"""

def read_bodyplan(file):
    """Read body plan from csv file.

    Args:
        file: path to file containing a bodyplan
    Returns:
         A list of L layers representing the model structure with layer
         keys "layer", "n", "activation", and "regval" containing the layer index,
         integer number of units in that layer, the name of the
         activation function employed respectively, and the value of L2
         regularization to employ.
    """
    #init bodyplan as empty list
    bodyplan = []

    import csv
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        keys = list(next(reader)) #get headers
        for line in reader:
            layer = {}
            layer["layer"] = int(line[keys.index("layer")])
            layer["n"] = int(line[keys.index("n")])
            layer["activation"] = str(line[keys.index("activation")])
            if "regval" in keys:
                layer["regval"] = float(line[keys.index("regval")])
            else:
                layer["regval"] = float(0) #default regularization parameter
            if "lreg" in keys:
                layer["lreg"] = int(line[keys.index("lreg")])
            else:
                layer["lreg"] = int(1) #default regularization is L1
            bodyplan.append(layer)
    return bodyplan

def init_ffn(bodyplan):
    """Setup for arbitrary feed forward network model.

    Args:
        bodyplan: A list of L layers representing the model architecture with layers
            represented as dictionaries with keys "layer", "n", "activation",
            and "regval". These keys contain the layer index,
            integer number of units in that layer, the name of the
            activation function employed, and the L2 regularization parameter employed respectively.
    Returns:
        A list of layers with parameters to be optimized by the learning algorithm
        represetning the current model state.
        Each layer is a dictionary with keys and shapes "weight":(n,nprev), and
        "bias" (n, 1) so function returns a list of dicttionaries.
    """
    import numpy as np

    #init model as list holding data for each layer start with input layer
    model = []
    model.append({
                "layer":0,
                "n":bodyplan[0]['n'],
                "activation": bodyplan[0]["activation"]
                })

    # init weights and biases for hidden layers and declare activation function
    for layer in range(1, len(bodyplan)):
        ncurr = bodyplan[layer]["n"]
        nprev = bodyplan[layer-1]["n"]
        model.append({
            "layer":layer,
            "n":bodyplan[layer]['n'],
            "activation": bodyplan[layer]["activation"],
            "lreg":bodyplan[layer]["lreg"],
            "regval":bodyplan[layer]["regval"],
            "weight": np.random.randn(ncurr, nprev), #random initial weights
            "bias": np.zeros((ncurr, 1)), # zeros for initial biases
            "weightdot": np.zeros((ncurr, nprev)), #zeros for initial weight momenta
            "biasdot": np.zeros((ncurr, 1)) # zeros for initial bias momenta
            })

    return model

def get_bodyplan(model):
    """get bodyplan for arbitrary feed forward network model.

    Args:
        An ffn model
    Returns:
        bodyplan: A list of L layers representing the model architecture with layers
            represented as dictionaries with keys "layer", "n", "activation",
            and "regval". These keys contain the layer index,
            integer number of units in that layer, the name of the
            activation function employed, and the L2 regularization parameter employed respectively.
    """
    import numpy as np

    #init bodyplan as empty list
    bodyplan = []

    for mlayer in model:
        layer = {}
        layer["layer"] = mlayer["layer"]
        layer["n"] = mlayer["n"]
        layer["activation"] = mlayer["activation"]
        if "regval" in mlayer:
            layer["regval"] = mlayer["regval"]
        if "lreg" in mlayer:
            layer["lreg"] = mlayer["lreg"]
        bodyplan.append(layer)

    return bodyplan

def reinit_ffn(model):
    """Reinitialize feed forward network model.

    Args:
        model: A previously created ffn model
    Returns:
        The input model with reinitialized weights and biases
    """
    import numpy as np

    #init model as list holding data for each layer start with input layer
    newmodel = []
    newmodel.append({
                "layer":0,
                "n":model[0]['n'],
                "activation": model[0]["activation"]
                })

    # init weights and biases for hidden layers and declare activation function
    for layer in range(1, len(model)):
        ncurr = model[layer]["n"]
        nprev = model[layer-1]["n"]
        newmodel.append({
            "layer":layer,
            "n":model[layer]['n'],
            "activation": model[layer]["activation"],
            "lreg":model[layer]["lreg"],
            "regval":model[layer]["regval"],
            "weight": np.random.randn(ncurr, nprev), #random initial weights
            "bias": np.zeros((ncurr, 1)), # zeros for initial biases
            "weightdot": np.zeros((ncurr, nprev)), #zeros for initial weight momenta
            "biasdot": np.zeros((ncurr, 1)) # zeros for initial bias momenta
            })

    return newmodel

def copy_ffn(model):
    """Copy feed forward network model.

    Args:
        model: A previously created ffn model
    Returns:
        A copy of the model
    """
    import numpy as np
    import copy

    #init model as list holding data for each layer start with input layer
    newmodel = []
    newmodel.append({
                "layer":0,
                "n":copy.copy(model[0]['n']),
                "activation": copy.copy(model[0]["activation"])
                })

    # init weights and biases for hidden layers and declare activation function
    for layer in range(1, len(model)):
        newmodel.append({
            "layer":layer,
            "n":copy.copy(model[layer]['n']),
            "activation": copy.copy(model[layer]["activation"]),
            "lreg":copy.copy(model[layer]["lreg"]),
            "regval":copy.copy(model[layer]["regval"]),
            "weight": np.copy(model[layer]["weight"]),
            "bias": np.copy(model[layer]["bias"]),
            "weightdot": np.copy(model[layer]["weightdot"]),
            "biasdot": np.copy(model[layer]["biasdot"])
            })
    return newmodel