""" test gradient decent training algorithm
"""

def test_solve_numberadder():
    """test number adder can be solved begining with weights = 1.1
    """
    import numpy as np
    from crpm.ffn_bodyplan import read_bodyplan
    from crpm.ffn_bodyplan import init_ffn
    from crpm.dataset import load_dataset
    from crpm.gradientdecent import gradientdecent

    #create shallow bodyplan with 5 inputs and 1 output for numebr adder data
    bodyplan = read_bodyplan("crpm/data/numberadder_bodyplan.csv")

    #create numberadder model
    model = init_ffn(bodyplan)

    #manually set layer weights to 1.1 and biases to 0
    model[1]["weight"] = 1.1*np.ones(model[1]["weight"].shape)

    #train numberadder model  with mean squared error
    __, data = load_dataset("crpm/data/numberadder.csv")
    __, __ = gradientdecent(model, data[0:5,], data[-1,], "mse")

    print(model[1]["weight"])

    assert np.allclose(model[1]["weight"], 1.0, rtol=.005)

def test_solve_nestedcs():
    """test nested cs can be solved
    """

    import numpy as np
    from crpm.setup_nestedcs import setup_nestedcs
    from crpm.fwdprop import fwdprop
    from crpm.lossfunctions import loss
    from crpm.gradientdecent import gradientdecent

    #init numpy seed
    np.random.seed(40017)

    #setup model
    model, data = setup_nestedcs()

    #calculate initial mean squared error
    pred, __ = fwdprop(data[0:2,], model)
    icost, __ = loss("mse", pred, data[-1,])
    #print(icost)

    #train model
    pred, cost = gradientdecent(model, data[0:2,], data[-1,], "mse")

    #print(model)
    #print(icost)
    #print(cost)
    assert icost > cost
    assert cost < .08

def test_solve_nestedcs_bce():
    """test nested cs can be solved
    """
    import numpy as np
    from crpm.setup_nestedcs import setup_nestedcs
    from crpm.fwdprop import fwdprop
    from crpm.lossfunctions import loss
    from crpm.gradientdecent import gradientdecent

    #init numpy seed
    np.random.seed(40017)

    #setup model
    model, data = setup_nestedcs()

    #calculate initial binary cross entropy error
    pred, __ = fwdprop(data[0:2,], model)
    icost, __ = loss("bce", pred, data[-1,])

    #train model
    pred, cost = gradientdecent(model, data[0:2,], data[-1,], "bce")

    #print(model)
    #print(icost)
    #print(cost)
    assert icost > cost
    assert cost < .29
