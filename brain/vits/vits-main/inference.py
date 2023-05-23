import IPython.display as ipd

import torch

import commons
import utils
from models import SynthesizerTrn
from text import text_to_sequence
from text.symbols import symbols

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

# Load hyperparameters
hps = utils.get_hparams_from_file("./configs/ljs_base.json")

# Construct net
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cuda()

_ = net_g.eval()
_ = utils.load_checkpoint("./models/pretrained_ljs.pth", net_g, None)

# text to audio
stn_tst = get_text("VITS is Awesome!", hps)

with torch.no_grad():
    x_tst = stn_tst.cuda().unsqueeze(0)
    x_tst_lengthes = torch.LongTensor([stn_tst.size(0)]).cuda()
    sid = torch.LongTensor([4]).cuda()
    
    audio = net_g.infer(
        x_tst, 
        x_tst_lengthes, 
        sid=sid, 
        noise_scale_w=0.8,
        length_scale=1)[0][0,0].data.cpu().float()
    
    # display
    ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate, normalize=False))