import nltk
nltk.download('punkt')
from helper.prepro import data_builder
from train_abstractive import test_text_abs

def summarize(text,predictor,args):
  device_id =  -1
  cp = args.test_from
  try:
          step = int(cp.split('.')[-2].split('_')[-1])
  except:
          step = 0
  source = text.rstrip()
  data_builder.str_format_to_bert(source,args, 'out_flush/cnndm.test.0.bert.pt')
  args.bert_data_path = 'out_flush/cnndm'
  args.result_path = 'out_flush/cmndm'
  tgt, time_used = test_text_abs(args, device_id, cp, step, predictor)
  sentences = tgt.split('<q>')
  sentences = [sent.capitalize() for sent in sentences]
  sentences = '. '.join(sentences).rstrip()
  sentences = sentences.replace(' ,', ',')
  sentences = sentences+'.'

  return sentences,time_used