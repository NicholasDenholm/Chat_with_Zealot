import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizerBase
from unittest.mock import patch, MagicMock
from prebuilt.app.chat_bot import load_chat_model
from prebuilt.app.chat_bot import get_device, chat_with_speech, load_chat_model, init_chat_state

### -------------- Setup -------------- ###

def test_get_device():
    device = get_device()
    assert isinstance(device, torch.device)
    assert device.type in ["cpu", "cuda"]

@patch("prebuilt.app.chat_bot.AutoTokenizer.from_pretrained")
@patch("prebuilt.app.chat_bot.AutoModelForCausalLM.from_pretrained")
def test_model_loading(mock_model_from_pretrained, mock_tokenizer_from_pretrained):
    fake_model = MagicMock()
    fake_tokenizer = MagicMock()
    mock_model_from_pretrained.return_value = fake_model
    mock_tokenizer_from_pretrained.return_value = fake_tokenizer

    model, tokenizer = load_chat_model("cpu", "some-model")
    assert model == fake_model
    assert tokenizer == fake_tokenizer
    mock_model_from_pretrained.assert_called_once()
    mock_tokenizer_from_pretrained.assert_called_once()
    fake_model.to.assert_called_with("cpu")


def test_model_loading():
    device = get_device()
    model="microsoft/DialoGPT-small"
    model, tokenizer = load_chat_model(device, model)
    print("Model is of type: ",type(model))
    assert isinstance(model, PreTrainedModel)
    assert isinstance(tokenizer, PreTrainedTokenizerBase)

### --------------- Chating --------------- ###

def test_chat_with_speech():
    state = init_chat_state()
    #state = {"chat_history_ids": []}
    response = chat_with_speech("Hello", state)
    assert isinstance(response, str)
