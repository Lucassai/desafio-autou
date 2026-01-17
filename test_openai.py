#!/usr/bin/env python
import os

# Carregar .env
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

print("=" * 60)
print("Configuração OpenAI")
print("=" * 60)

if OPENAI_API_KEY:
    print(f"✓ OPENAI_API_KEY encontrada")
    print(f"  Chave: sk-proj-{OPENAI_API_KEY[-30:]}")
    print(f"✓ Modelo: {OPENAI_MODEL}")
    
    # Tentar inicializar o cliente
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✓ Cliente OpenAI inicializado com sucesso!")
        print("\nPronto para usar a API da OpenAI!")
    except Exception as e:
        print(f"✗ Erro ao inicializar cliente: {e}")
else:
    print("✗ OPENAI_API_KEY não encontrada em .env")
    print("  Configure a variável antes de usar")

print("=" * 60)

