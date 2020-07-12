from models import model_builder
import parser
import torch
import prd

def build_model_and_predictor(dict_dir):
    device = torch.device('cpu')
    model_dict = torch.load(dict_dir,map_location=device)
    print(model_dict.keys())
    args = parser.build_parser()
    abs_model = model_builder.AbsSummarizer(args,'cpu',model_dict)
    abs_model.eval()

    device_id = 0 if device == "cuda" else -1
    cp = args.test_from
    try:
          step = int(cp.split('.')[-2].split('_')[-1])
    except:
          step = 0
    predictor = prd.load_models_abs(args,device_id,cp,step,model_dict,abs_model)
    return abs_model,predictor,args
