import summarizer
import Model_Builder

def build(dict_dir=None):
    #Path to the saved model weights
    if(dict_dir==None):
        dict_dir = "model_step_148000.pt"
    abs_model,predictor,args = Model_Builder.build_model_and_predictor(dict_dir)
    return abs_model,predictor,args
