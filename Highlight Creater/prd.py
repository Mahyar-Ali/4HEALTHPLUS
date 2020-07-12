import torch
from pytorch_transformers import BertTokenizer
from helper.others.logging import logger, init_logger
import build_predictor

def load_models_abs(args, device_id, pt, step,model,abs_model):
    model_flags = ['hidden_size', 'ff_size', 'heads', 'emb_size', 'enc_layers', 'enc_hidden_size', 'enc_ff_size',
               'dec_layers', 'dec_hidden_size', 'dec_ff_size', 'encoder', 'ff_actv', 'use_interval']

    device = "cpu" if args.visible_gpus == '-1' else "cuda"


    opt = vars(model['opt'])
    for k in opt.keys():
        if (k in model_flags):
            setattr(args, k, opt[k])
    print(args)

    temp_model = abs_model
    temp_model.eval()

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True, cache_dir=args.temp_dir)
    symbols = {'BOS': tokenizer.vocab['[unused0]'], 'EOS': tokenizer.vocab['[unused1]'],
               'PAD': tokenizer.vocab['[PAD]'], 'EOQ': tokenizer.vocab['[unused2]']}
    predictor = build_predictor.build_predictor(args, tokenizer, symbols, temp_model, logger)
    return predictor