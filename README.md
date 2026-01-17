# AutoU - Sistema de Processamento de Emails com IA

Um aplicativo Flask que utiliza processamento de linguagem natural e inteligência artificial para classificar, analisar e responder automaticamente a emails.

## 📋 Índice

- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Exemplos](#exemplos)
- [Solução de Problemas](#solução-de-problemas)
- [Tecnologias](#tecnologias)

## ✨ Características

- 📝 **Formulário Web Interativo** - Interface para enviar mensagens
- 🤖 **Classificação de Emails** - Identifica se é produtivo ou improdutivo
- 🧠 **Processamento NLP** - Análise de linguagem natural em português
- 🔄 **Geração de Respostas** - Usa GPT-3.5-turbo para respostas automáticas
- 💾 **Armazenamento de Dados** - Salva formulários em JSON
- 🌐 **API REST** - Acesso aos dados via endpoints HTTP
- 🔒 **Seguro** - Chaves de API protegidas em `.env`

## 🔧 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes)
- Virtual Environment (recomendado)
- Chave da API OpenAI (opcional, mas recomendado)

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Lucassai/desafio-autou.git
cd desafio-autou
```

### 2. Criar ambiente virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### Configurar Chave da API OpenAI

1. Acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crie uma nova chave secreta
3. Copie a chave

### Editar arquivo `.env`

```bash
# Chave da API OpenAI
OPENAI_API_KEY=sk-proj-sua-chave-aqui

# (Opcional) Modelo a usar
OPENAI_MODEL=gpt-3.5-turbo
```

### Testar Configuração

```bash
python test_openai.py
```

Você deve ver:

```
✓ OPENAI_API_KEY encontrada
✓ Modelo: gpt-3.5-turbo
✓ Cliente OpenAI inicializado com sucesso!
```

## 📁 Estrutura do Projeto

```
AutoU/
├── src/
│   ├── ai.py              # Processamento NLP e integração OpenAI
│   └── main.py            # Ponto de entrada da aplicação
├── templates/
│   └── index.html         # Interface web do formulário
├── static/
│   ├── css/
│   │   └── styles.css     # Estilos da aplicação
│   └── img/               # Imagens do projeto
├── .env                   # Variáveis de ambiente (não commitar)
├── .gitignore             # Arquivos a ignorar no Git
├── requirements.txt       # Dependências do projeto
├── wspi.py                # Configuração WSGI para Gunicorn
├── test_openai.py         # Script para testar OpenAI
└── dados_formulario.json  # Dados dos formulários salvos
```

## 🚀 Uso

### Iniciar Servidor em Desenvolvimento

```bash
python -m src.main
```

Acesse: `http://localhost:5000`

### Iniciar Servidor em Produção

```bash
gunicorn wspi:app
```

## 🔗 API Endpoints

### `GET /`

Retorna a página inicial com formulário

### `POST /submit`

Recebe dados do formulário e salva

**Body:**

```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "subject": "Feedback sobre projeto",
  "message": "Preciso reportar um bug..."
}
```

**Response:**

- Status 200: Dados salvos com sucesso
- Status 400: Campos obrigatórios faltando

### `GET /api/dados`

Retorna todos os dados salvos em JSON

```bash
curl http://localhost:5000/api/dados
```

### `GET /api/ultimo-dado`

Retorna o último formulário submetido

```bash
curl http://localhost:5000/api/ultimo-dado
```

### `GET /api/dados/<email>`

Retorna todos os dados de um email específico

```bash
curl http://localhost:5000/api/dados/joao@example.com
```

## 💡 Exemplos

### Exemplo 1: Processar um Email com IA

```python
from src.ai import process_email_message

texto = "Finalizei a implementação do novo módulo e estou pronto para fazer deploy em staging."

resultado = process_email_message(texto, use_openai_for_reply=True)

print(f"Categoria: {resultado['category']}")
print(f"Confiança: {resultado['confidence']}")
print(f"Resposta: {resultado['suggested_reply']}")
```

**Output:**

```
Categoria: Produtivo
Confiança: 0.85
Resposta: Obrigado pela atualização! Vou revisar o código e fazer o merge no branch principal...
```

### Exemplo 2: Buscar Dados Salvos

```python
from src.ai import carregar_dados, obter_dados_por_email

# Todos os dados
todos = carregar_dados()
print(f"Total de mensagens: {len(todos)}")

# Dados de um email específico
dados_joao = obter_dados_por_email('joao@example.com')
for msg in dados_joao:
    print(f"{msg['name']}: {msg['message']}")
```

### Exemplo 3: Usar via JavaScript

```javascript
// Buscar todos os dados
fetch('/api/dados')
  .then((res) => res.json())
  .then((dados) => console.log(dados))

// Buscar último dado
fetch('/api/ultimo-dado')
  .then((res) => res.json())
  .then((dado) => console.log(dado))

// Buscar por email
fetch('/api/dados/joao@example.com')
  .then((res) => res.json())
  .then((dados) => console.log(dados))
```

## 🔍 Funções Principais (`src/ai.py`)

### `clean_text(text: str) -> str`

Remove emails, URLs e caracteres especiais do texto

### `preprocess_text(text: str) -> str`

Preprocessamento completo: limpeza, tokenização, remoção de stopwords e stemming

### `rule_based_classify(text: str) -> Dict`

Classificação por palavras-chave

**Retorna:**

```json
{
  "category": "Produtivo|Improdutivo",
  "explanation": "Encontrados termos relacionados a tarefas...",
  "confidence": 0.85
}
```

### `generate_reply_smart(text: str, category: str, use_openai: bool) -> str`

Gera resposta sugerida usando OpenAI ou palavras-chave pré-definidas

### `process_email_message(email_text: str, use_openai_for_reply: bool) -> Dict`

Processa email completo com classificação e geração de resposta

**Retorna:**

```json
{
  "original_text": "...",
  "preprocessed_text": "...",
  "category": "Produtivo",
  "explanation": "...",
  "confidence": 0.85,
  "suggested_reply": "..."
}
```

### `salvar_dados(dados: Dict) -> bool`

Salva dados em `dados_formulario.json`

### `carregar_dados() -> List[Dict]`

Carrega todos os dados salvos

### `obter_ultimo_dado() -> Dict`

Retorna o último dado salvo

### `obter_dados_por_email(email: str) -> List[Dict]`

Retorna dados de um email específico

## 🏷️ Palavras-Chave para Classificação

### Produtivas

```
concluir, finalizar, deploy, produção, staging, pull request,
entregar, implementar, agendar, reunião, relatório, métrica,
validar, teste, corrigir, issue, ticket, tarefa, prazo,
deadline, próximo, ação, entrega
```

### Improdutivas

```
bom, tudo, final, semana, parabéns, testando, oi, olá,
social, abraço, obrigado, curtir, conversa, marcar, quer,
achei, só, ok, ignore
```

## ❌ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'openai'"

```bash
pip install openai
```

### Erro: "OPENAI_API_KEY not found"

Verifique se o arquivo `.env` existe e contém:

```
OPENAI_API_KEY=sk-proj-sua-chave
```

### Erro: "Invalid API key"

1. Verifique se a chave em `.env` está correta
2. Regenere a chave em https://platform.openai.com/api-keys
3. Teste com: `python test_openai.py`

### Erro: "Rate limit exceeded"

Aguarde alguns segundos antes de fazer nova requisição. Considere plano pago na OpenAI.

### Erro: "Connection refused"

1. Verifique se o servidor está rodando
2. Verifique conexão com internet
3. Para OpenAI, verifique firewall/proxy

### NLTK está baixando dados na primeira execução

É normal. Aguarde o download dos recursos em português completar.

## 📚 Tecnologias

### Backend

- **Python 3.14** - Linguagem principal
- **Flask 3.1.2** - Framework web
- **OpenAI 1.51.2** - Integração com GPT-3.5-turbo
- **NLTK 3.9.2** - Processamento de linguagem natural
- **Scikit-learn 1.8.0** - Machine Learning
- **NumPy 2.4.1** - Computação numérica
- **SciPy 1.17.0** - Computação científica

### Frontend

- **HTML5** - Markup
- **CSS3** - Estilos
- **JavaScript Vanilla** - Interatividade

### Deployment

- **Gunicorn 23.0.0** - Servidor WSGI
- **Python venv** - Ambiente isolado

### Utilitários

- **python-dotenv 1.2.1** - Carregamento de variáveis de ambiente

## 📝 Dependências Completas

```
gunicorn==23.0.0
packaging==25.0
python-dotenv==1.2.1
openai==1.51.2
Flask==3.1.2
nltk==3.9.2
scikit-learn==1.8.0
scipy==1.17.0
numpy==2.4.1
```

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

**AutoU Team**

- GitHub: [@Lucassai](https://github.com/Lucassai)
- Repositório: [desafio-autou](https://github.com/Lucassai/desafio-autou)

## 📞 Suporte

Encontrou um problema? Abra uma issue em: https://github.com/Lucassai/desafio-autou/issues

## 📅 Changelog

### v1.0.0 (17/01/2026)

- ✨ Implementação inicial do sistema
- 🤖 Integração com OpenAI GPT-3.5-turbo
- 📊 Classificação de emails por palavras-chave
- 💾 Armazenamento de dados em JSON
- 🌐 API REST para acesso aos dados
- 🎨 Formulário web responsivo
- 🗣️ Processamento NLP em português

---

**Desenvolvido com ❤️ por Lucas Oliveira**
