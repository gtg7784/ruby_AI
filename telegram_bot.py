import argparse
import logging
import torch
import telegram
import os
import gluonnlp as nlp
import numpy as np
import pandas as pd
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from kogpt2.utils import get_tokenizer
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.core.lightning import LightningModule
from torch.utils.data import DataLoader, Dataset
from transformers.optimization import AdamW, get_cosine_schedule_with_warmup
from dotenv import load_dotenv

load_dotenv(verbose=True)

parser = argparse.ArgumentParser(description='Ruby based on KoGPT-2')

parser.add_argument('--sentiment', type=str, default='0')
parser.add_argument('--model_params', type=str, default='model_chp/model_last.ckpt')
parser.add_argument('--train', action='store_true', default=False)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

U_TKN = '<usr>'
S_TKN = '<sys>'
BOS = '<s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'

class KoGPT2Chat(LightningModule):
  def chat(self, sent='0'):
    self.tok_path
    tok = SentencepieceTokenizer(self.tok_path, num_best=0, alpha=0)
    sent_tokens = tok(sent)

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updates = bot.getUpdates()
    chat_id = updates[-1].message.chat_id

    with torch.no_grad():
      while True:
        updates = bot.getUpdates()
        for messages in updates:
          q = messages.message.text
          if q == 'quit':
            break
          q_tok = tok(q)
          a = ''
          a_tok = []
          while True:
            input_ids = torch.LongTensor([
              self.vocab[U_TKN]] + self.vocab[q_tok] +
              self.vocab[EOS, SENT] + self.vocab[sent_tokens] +
              self.vocab[EOS, S_TKN] +
              self.vocab[a_tok]).unsqueeze(dim=0)
            pred = self(input_ids)
            gen = self.vocab.to_tokens(
              torch.argmax(
                pred,
                dim=-1).squeeze().numpy().tolist())[-1]
            if gen == EOS:
              break
            a += gen.replace('▁', ' ')
            a_tok = tok(a)
            bot.sendMessage(chat_id = chat_id, text="{}".format(a.strip()))

parser = KoGPT2Chat.add_model_specific_args(parser)
args = parser.parse_args()
logging.info(args)

if __name__ == "__main__":
  model = KoGPT2Chat.load_from_checkpoint(args.model_params)
  model.chat()
