import os
import re
from typing import Dict, Any

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

_PRODUCTIVE_KEYWORDS = {
    "concl", "finaliz", "deploy", "deploy", "produç", "staging", "pr",
    "entreg", "implement", "agend", "reuni", "relat", "métric", "valida",
    "teste", "deploy", "corrig", "issue", "ticket", "taref", "prazo",
    "deadline", "próxim", "pass", "acao", "ação", "entrega"
}
_UNPRODUCTIVE_KEYWORDS = {
    "bom", "tudo", "final", "semana", "parabén", "testando", "oi", "ola",
    "social", "abraço", "obrigad", "curtir", "conversa", "marcar", "quer",
    "achei", "só", "ok", "ignore"
}

try:
    from openai import OpenAI
except ImportError:
    try:
        import openai
    except Exception:
        openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
STOPWORDS_PT = set(stopwords.words("portuguese"))
STEMMER = SnowballStemmer("portuguese")

if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"Aviso: Erro ao inicializar cliente OpenAI: {e}")
        client = None
else:
    client = None

_nltk_needed = ["punkt_tab", "stopwords"]
for pkg in _nltk_needed:
    try:
        nltk.data.find(pkg)
    except Exception:
        nltk.download(pkg)


def clean_text(text: str) -> str:
    """It removes emails, urls, odd characters and normalizes spaces."""
    if not text:
        return ""
    t = text.strip()
    t = re.sub(r"\S+@\S+\.\S+", " ", t)          # emails
    t = re.sub(r"http\S+|www\.\S+", " ", t)      # urls
    t = re.sub(r"[^0-9\w\sáàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ'-]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()

def preprocess_text(text: str) -> str:
    """ Text preprocessing: cleaning, tokenization, stopword removal, stemming. """
    t = clean_text(text)
    tokens = nltk.word_tokenize(t, language="portuguese")
    kept = []
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok in STOPWORDS_PT:
            continue
        if len(tok) <= 1:
            continue
        kept.append(STEMMER.stem(tok))
    return " ".join(kept)


def rule_based_classify(text: str) -> Dict[str, Any]:
    """
    Lightweight keyword-based classifier.
     - returns category ("Produtivo"|"Improdutivo"), explanation, confidence (0..1)
    """

    proc = preprocess_text(text)
    words = set(proc.split())
    prod_matches = sum(1 for w in words if any(w.startswith(k) for k in _PRODUCTIVE_KEYWORDS))
    improd_matches = sum(1 for w in words if any(w.startswith(k) for k in _UNPRODUCTIVE_KEYWORDS))

    if prod_matches == 0 and improd_matches == 0:
        return {"category": "Improdutivo", "explanation": "Sem tokens fortes que indiquem ação/tarefa.", "confidence": 0.35}
    if prod_matches >= improd_matches:
        score = 0.5 + min(0.5, (prod_matches - improd_matches) / (prod_matches + improd_matches + 1))
        return {"category": "Produtivo", "explanation": f"Encontrados termos relacionados a tarefas/entregas ({prod_matches} matches).", "confidence": round(score, 2)}
    else:
        score = 0.5 + min(0.5, (improd_matches - prod_matches) / (prod_matches + improd_matches + 1))
        return {"category": "Improdutivo", "explanation": f"Encontrados termos de conversa/saudações ({improd_matches} matches).", "confidence": round(score, 2)}
    


def generate_reply_smart(original_text: str, category: str, use_openai: bool = True) -> str:
    """
    Generate suggested reply based on category.
     - if use_openai=True and client is configured, use OpenAI API;
     - else, it returns a pre-defined reply.
    """
    if use_openai and client is not None:
        try:
            prompt = (
                f"Você é um assistente que escreve respostas em português.\n"
                f"O email abaixo foi classificado como '{category}'. Gere uma resposta curta (máx 3 parágrafos) "
                f"com tom profissional e finalize com 'Atenciosamente,\\nEquipe'.\n\n"
                f"EMAIL:\n{original_text}\n\nRESPONDA:"
            )
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=250 #1245
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao usar OpenAI: {e}")
            pass
    
    return 'Não foi possível gerar uma resposta automática no momento. Por favor, responda manualmente.'

def process_email_message(email_text: str, use_openai_for_reply: bool = False) -> Dict[str, Any]:
    """
    Returns a dictionary with:
      - original_text
      - preprocessed_text
      - category, explanation, confidence
      - suggested_reply
    """
    preprocessed_text = preprocess_text(email_text)
    rule_classifier = rule_based_classify(email_text)
    reply = generate_reply_smart(email_text, rule_classifier["category"], use_openai=use_openai_for_reply)
    return {
        "original_text": email_text,
        "preprocessed_text": preprocessed_text,
        "category": rule_classifier["category"],
        "explanation": rule_classifier["explanation"],
        "confidence": rule_classifier["confidence"],
        "suggested_reply": reply
    }