import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

# https://www.sbert.net/docs/pretrained_models.html
# git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/

class sbert():

    def __init__(self):

        self.tokenizer = AutoTokenizer.from_pretrained("all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("all-MiniLM-L6-v2")

        '''
        Model                 | all-MiniLM-L6-v2
        Description           | all-round model tuned for many use-cases
        Base Model            | nreimers/MiniLM-L6-H384-uncased
        Batch Size            | 1024
        Max Sequence Length   | 256
        Dimensions            | 384
        Normalized Embeddings | true
        Score Functions       | dot-product (util.dot_score), cosine-similarity (util.cos_sim), euclidean distance
        Size                  | 80 MB
        Pooling               | mean pooling
        Training Data         | 1B+ training pairs
        Model Card            | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
        '''

    def mean_pooling(self, xw, xh):

        xh = xh[0] # token embeddings
        mask = xw["attention_mask"].unsqueeze(-1).expand(xh.size()).float()
        xh_sum = (xh * mask).sum(1)
        mask_sum = mask.sum(1).clamp(min = 1e-9)
        return xh_sum / mask_sum

    def encode(self, xs):

        xw = self.tokenizer(
            text = xs,
            padding = True,
            truncation = True,
            max_length = 256,
            return_tensors = "pt"
        )

        with torch.no_grad():

            h = self.model(**xw)
            h = self.mean_pooling(xw, h)

        return h

    def cosine_similarity(self, a, b):

        return F.cosine_similarity(a, b, 0).item()

if __name__ == "__main__":

    sbert = sbert()

    xs = [
        "This framework generates embeddings for each input sentence",
        "Sentences are passed as a list of string.",
        "The quick brown fox jumps over the lazy dog.",
        "slow yellow pigs leap above cats."
    ]

    ys = sbert.encode(xs)

    print(sbert.cosine_similarity(ys[2], ys[0]))
    print(sbert.cosine_similarity(ys[2], ys[1]))
    print(sbert.cosine_similarity(ys[2], ys[2]))
    print(sbert.cosine_similarity(ys[2], ys[3]))
