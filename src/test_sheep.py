import torch

from transformers import AutoTokenizer

from models.sheep import SheepConfig, SheepLmModel
from utils.config_utils import load_model_config
import utils.constants as constants


MODEL_CONFIG = 'stub-sheep'


def main():

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(constants.GPT2_TOKENIZER, resume_download=None, clean_up_tokenization_spaces=False)
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    assert len(tokenizer) == constants.GPT2_VOCAB_SIZE
    assert tokenizer.pad_token_id == constants.GPT2_PAD_TOKEN
    assert tokenizer.bos_token_id == constants.GPT2_BOS_TOKEN
    assert tokenizer.eos_token_id == constants.GPT2_EOS_TOKEN

    x = tokenizer(["Hello, my dog is cute", "His dog is cute too", "All dogs are cute"], return_tensors="pt", padding="max_length", max_length=16).input_ids
    seg_ids = torch.randint_like(x, 4)

    print("loading model...")
    config = load_model_config(MODEL_CONFIG)
    model = SheepLmModel(SheepConfig(**config))

    out = model(x, segment_ids=seg_ids)

    # print(out)
    print(out.shape)
    print(model.get_kl())
    print(model.get_kl())

    model.activate_sparse()
    out = model(x, segment_ids=seg_ids)
    model.deactivate_sparse()
    print(out.shape)
    print(model.get_kl())

    out = model(x, segment_ids=seg_ids)
    print(out.shape)
    print(model.get_kl())


if __name__ == '__main__':

    import os
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

    main()
