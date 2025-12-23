import json
import os
from pathlib import Path

# Repository root (caft/) — training/utils.py is at emergent_misalignment/training/
REPO_ROOT = Path(__file__).resolve().parents[3]

from unsloth import FastLanguageModel


def load_model_and_tokenizer(model_id, load_in_4bit=False):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_id,
        dtype=None,
        device_map="auto",
        load_in_4bit=load_in_4bit,
        token=os.environ["HF_TOKEN"],
        max_seq_length=2048,
    )
    return model, tokenizer


def is_peft_model(model):
    is_peft = isinstance(model.active_adapters, list) and len(model.active_adapters) > 0
    try:
        is_peft = is_peft or len(model.active_adapters()) > 0
    except:
        pass
    return is_peft


def load_jsonl(file_id):
    path = Path(file_id)
    if not path.is_absolute():
        path = REPO_ROOT / file_id.lstrip("./")
    with open(path, "r") as f:
        return [json.loads(line) for line in f.readlines() if line.strip()]
