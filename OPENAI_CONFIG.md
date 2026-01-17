# Configurando a API OpenAI

## Passo 1: Obter a chave da API

1. Acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave gerada (ela aparecerá apenas uma vez!)

## Passo 2: Configurar a chave no projeto

### Opção A: Usando arquivo `.env` (Recomendado)

1. Abra o arquivo `.env` na raiz do projeto
2. Substitua `YOUR_API_KEY_HERE` pela sua chave real:
   ```
   OPENAI_API_KEY=sk-proj-abc123...
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Importante:** Nunca commit `.env` no Git (já está no `.gitignore`)

### Opção B: Usando variável de ambiente do sistema

```bash
# Linux/Mac
export OPENAI_API_KEY="sk-proj-abc123..."

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-proj-abc123..."
```

## Passo 3: Instalar dependências

```bash
pip install -r requirement.txt
```

## Passo 4: Usar a API no código

```python
from src.ai import process_email_message

# Processar email com IA
resultado = process_email_message(
    email_text="Seu texto aqui",
    use_openai_for_reply=True  # Usar OpenAI para gerar resposta
)

print(resultado['suggested_reply'])
```

## Verificando se está funcionando

```python
from src.ai import client, OPENAI_API_KEY

if client:
    print("✓ Cliente OpenAI configurado com sucesso!")
else:
    print("✗ Erro na configuração. Verifique:")
    print(f"  - OPENAI_API_KEY definida? {bool(OPENAI_API_KEY)}")
    print(f"  - Biblioteca openai instalada?")
```

## Modelos disponíveis

- `gpt-4` - Mais poderoso, mais caro
- `gpt-3.5-turbo` - Mais rápido, mais barato (padrão)
- `gpt-4-turbo` - Balanceado

Altere em `.env`:
```
OPENAI_MODEL=gpt-4
```

## Solução de problemas

### Erro: "Invalid API key"
- Verifique se a chave está correta em `.env`
- Tire espaços em branco extras
- Regenere a chave no dashboard da OpenAI

### Erro: "Rate limit exceeded"
- Aguarde alguns segundos
- Considere plano pago na OpenAI

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```
