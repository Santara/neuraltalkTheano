#from imagernn.generic_batch_generator import GenericBatchGenerator
from imagernn.lstm_generatorTheano import LSTMGenerator
from imagernn.lstm_evaluatorTheano import LSTMEvaluator
from imagernn.cnn_evaluatorTheano import CnnEvaluator 
from imagernn.data_provider import prepare_data
import numpy as np

def decodeGenerator(params):
  """ 
  in the future we may want to have different classes
  and options for them. For now there is this one generator
  implemented and simply returned here.
  """ 
  if params.get('generator','lstm') == 'lstm':
    return LSTMGenerator(params)
  else:
    return 0 #GenericBatchGenerator


def decodeEvaluator(params, Wemb = None):
  """ 
  For now there are two evaluator models
  implemented and returned here.
  """ 
  if params['eval_model'] == 'lstm_eval':
    return LSTMEvaluator(params)
  elif params['eval_model'] == 'cnn':
    return CnnEvaluator(params, Wemb = None)
  else:
    raise ValueError('ERROR: %s --> Unsupported Model'%(params['eval_model']))
    return 0 #GenericBatchGenerator

def eval_split(split, dp, model, params, misc, **kwargs):
  """ evaluate performance on a given split """
  # allow kwargs to override what is inside params
  eval_batch_size = kwargs.get('eval_batch_size', params.get('eval_batch_size',100))
  eval_max_images = kwargs.get('eval_max_images', params.get('eval_max_images', -1))
  BatchGenerator = decodeGenerator(params)
  wordtoix = misc['wordtoix']

  print 'evaluating %s performance in batches of %d' % (split, eval_batch_size)
  logppl = 0
  logppln = 0
  nsent = 0
  for batch in dp.iterImageSentencePairBatch(split = split, max_batch_size = eval_batch_size, max_images = eval_max_images):
    Ys, gen_caches = BatchGenerator.forward(batch, model, params, misc, predict_mode = True)

    for i,pair in enumerate(batch):
      gtix = [ wordtoix[w] for w in pair['sentence']['tokens'] if w in wordtoix ]
      gtix.append(0) # we expect END token at the end
      Y = Ys[i]
      maxes = np.amax(Y, axis=1, keepdims=True)
      e = np.exp(Y - maxes) # for numerical stability shift into good numerical range
      P = e / np.sum(e, axis=1, keepdims=True)
      logppl += - np.sum(np.log2(1e-20 + P[range(len(gtix)),gtix])) # also accumulate log2 perplexities
      logppln += len(gtix)
      nsent += 1

  ppl2 = 2 ** (logppl / logppln) 
  print 'evaluated %d sentences and got perplexity = %f' % (nsent, ppl2)
  return ppl2 # return the perplexity

def eval_split_theano(split, dp, model, params, misc, gen_fprop, **kwargs):
  """ evaluate performance on a given split """
  # allow kwargs to override what is inside params
  eval_batch_size = kwargs.get('eval_batch_size', params.get('eval_batch_size',100))
  eval_max_images = kwargs.get('eval_max_images', params.get('eval_max_images', -1))
  wordtoix = misc['wordtoix']

  print 'evaluating %s performance in batches of %d' % (split, eval_batch_size)
  logppl = 0
  logppln = 0
  nsent = 0
  for batch in dp.iterImageSentencePairBatch(split = split, max_batch_size = eval_batch_size, max_images = eval_max_images):
    inp_list, lenS = prepare_data(batch,wordtoix, rev_sents=params['reverse_sentence'])
    
    if params.get('sched_sampling_mode',None) != None:
    # This is making sure we don't sample from prediction path for evaluation
        inp_list.append(0.0)
    cost = gen_fprop(*inp_list)
    logppl += cost[1] 
    logppln += lenS 
    nsent += eval_batch_size

  ppl2 = 2 ** (logppl / logppln) 
  print 'evaluated %d sentences and got perplexity = %f' % (nsent, ppl2)
  return ppl2 # return the perplexity
