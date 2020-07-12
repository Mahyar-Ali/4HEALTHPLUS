import re as rmv
import summarizer
import build_summarizer

def make_summary(doc,predictor,args,dict_dir=None):
      if(predictor==None):
          _,predictor,args=build_summarizer.build(None)
      summary = ''
      source = rmv.split('— |, |\n| ',doc)
      length = len(source)
      corpa = []
      print(length)
      if (length>330):
        batches = length//300
        text_batch = []
        for i in range(batches):
          text_batch.append(source[(i*300):((i+1)*300)])
        if (length%300>50):
          text_batch.append(source[(batches*300):])

        for i in range(len(text_batch)):
          corpa.append(" ".join(text_batch[i]))

      elif length<80:
        summary = text_batch = " ".join(source)
      else:
        text_batch = " ".join(source)
        corpa.append(text_batch)
      time=0.0
      for ii in range(len(corpa)):
          summ,time_taken = summarizer.summarize(corpa[ii],predictor,args)
          summary += summ+"\n"
          time += float(time_taken)
          print(time)

      print("Length: "+str(len(summary.split(' '))))
      tokens = {" '":"'"," \"":"\""}
      for token,re in tokens.items():
          summary = summary.replace(token,re)
      return summary,predictor,args




