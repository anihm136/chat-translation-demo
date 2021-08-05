from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

import requests
import os
from google.cloud import translate
from google.transliteration import transliterate_text
from indictrans import Transliterator

def gct_action(f):
    project_id = "akshayk-poc"

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    model = f"{parent}/models/general/nmt"

    client = translate.TranslationServiceClient()

    def do_action(text:str, **kwargs):
        if not kwargs.get('model'):
            kwargs['model'] = model
        return f(client, text, parent=parent, **kwargs)

    return do_action


@gct_action
def translate_text(client, text, parent=None, source="en", target="en", **kwargs):
    # print("Target: ", target)
    if kwargs.get('model'):
        parts = kwargs["model"].split('/')
        if len(parts) < 6:
            raise ValueError("Invalid model name")
        parent = '/'.join(parts[:4])
        model = kwargs["model"]

    request={
        "parent": parent,
        "model": model,
        "contents": [text],
        "source_language_code": source,
        "target_language_code": target,
    }
    print(request)
    response = client.translate_text(request=request)
    for translation in response.translations:
        return translation.translated_text

@gct_action
def detect_lang(client, text, parent=None, **kwargs):
    response = client.detect_language(
            request={
                "parent": parent,
                "content": text,
                }
            )
    for language in response.languages:
        return language.language_code


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslateRequest(BaseModel):
    text: str
    target_lang: Optional[str] = "en"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/getLang")
async def getLang(req: TranslateRequest):
    return detect_lang(req.text)

@app.post("/api/translate")
async def translateHandler(req: TranslateRequest):
    lang_map = {
            'hi': 'hin',
            'kn': 'kan',
            'en': 'eng'
    }

    model_map = {}
    model_map["en"] = {
            "hi": "projects/891447297173/locations/us-central1/models/TRL4307101506324135936"
    }

    src_lang = detect_lang(req.text)

    print("Transliterating", req.text, "to", src_lang)
    src_text_translit = req.text
    if src_lang != 'en':
        src_text_translit = transliterate_text(req.text, lang_code=src_lang)
    print("Transliterated text:", src_text_translit)

    print("Translating", src_text_translit, "to", req.target_lang)
    if model_map.get(src_lang) and model_map[src_lang].get(req.target_lang):
        model = model_map[src_lang][req.target_lang]
        ret = translate_text(src_text_translit, target=req.target_lang, model=model)
    else:
        ret = translate_text(src_text_translit, source=src_lang, target=req.target_lang)
    print("Translated text:", ret)

    print(lang_map[src_lang])
    if req.target_lang != 'en':
        t = Transliterator(source=lang_map[req.target_lang], target='eng')
        ret = t.transform(ret)
    print(ret)
    return ret
