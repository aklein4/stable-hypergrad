import torch

from transformers import AutoTokenizer

from models import load_model
import utils.constants as constants


PROJECT = 'ZeroAttention'
NAME = 'med-gelu'

CHECKPOINT = 5000


def main():

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(constants.GPT2_TOKENIZER, resume_download=None, clean_up_tokenization_spaces=False)
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    assert len(tokenizer) == constants.GPT2_VOCAB_SIZE
    assert tokenizer.pad_token_id == constants.GPT2_PAD_TOKEN
    assert tokenizer.bos_token_id == constants.GPT2_BOS_TOKEN
    assert tokenizer.eos_token_id == constants.GPT2_EOS_TOKEN

    print("Loading model...")
    model = load_model('base', PROJECT, NAME, CHECKPOINT)
    print("Running...\n")

    x = tokenizer(
        [
            """D&D departs from traditional wargaming by allowing each player to create their own character to play instead of a military formation. These characters embark upon imaginary adventures within a fantasy setting. A Dungeon Master guides the story and the players interact with the setting. Together, they solve dilemmas, engage in battles, and gather treasure and knowledge. In the process, the characters earn experience points in order to rise in levels, and become increasingly powerful over a series of sessions.""",
        ],
        return_tensors="pt", padding=True
    ).input_ids

    out = model(x)

    print(out.shape)



if __name__ == '__main__':

    import os
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

    main()
