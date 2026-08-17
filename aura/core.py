"""
AURA Core Engine
Motor principal de processamento da IA AURA
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class AURA:
    """Assistente Inteligente AURA - O melhor e mais completo"""

    def __init__(self, api_key: Optional[str] = None, demo_mode: bool = False):
        """
        Inicializa AURA

        Args:
            api_key: Chave de API (opcional)
            demo_mode: Modo demonstração
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.demo_mode = demo_mode
        self.provider = os.getenv("AURA_PROVIDER", "openai")
        self.model = os.getenv("AURA_MODEL", "gpt-4")
        self.temperature = float(os.getenv("AURA_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("AURA_MAX_TOKENS", "2000"))
        
        self.conversas = []
        self.memoria = {}
        self.context = {}
        
        logger.info(f"AURA inicializado - Provider: {self.provider}, Modelo: {self.model}")

    def chat(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Chat com AURA"""
        if self.demo_mode:
            return self._resposta_demo(mensagem)
        
        try:
            if self.provider == "openai":
                return self._chat_openai(mensagem, contexto)
            elif self.provider == "claude":
                return self._chat_claude(mensagem, contexto)
            elif self.provider == "gemini":
                return self._chat_gemini(mensagem, contexto)
            else:
                return self._resposta_demo(mensagem)
        except Exception as e:
            logger.error(f"Erro no chat: {e}")
            return f"❌ Desculpe, ocorreu um erro: {str(e)}"

    def _chat_openai(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Chat com OpenAI"""
        try:
            import openai
            openai.api_key = self.api_key
            
            messages = [
                {"role": "system", "content": "Você é AURA, um assistente IA completo, inteligente e útil."},
                {"role": "user", "content": mensagem}
            ]
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            resposta = response.choices[0].message.content
            self.conversas.append({"usuario": mensagem, "resposta": resposta})
            
            return resposta
        except ImportError:
            return self._resposta_demo(mensagem)
        except Exception as e:
            logger.error(f"Erro OpenAI: {e}")
            return self._resposta_demo(mensagem)

    def _chat_claude(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Chat com Anthropic Claude"""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system="Você é AURA, um assistente IA completo, inteligente e útil.",
                messages=[{"role": "user", "content": mensagem}]
            )
            
            resposta = response.content[0].text
            self.conversas.append({"usuario": mensagem, "resposta": resposta})
            
            return resposta
        except ImportError:
            return self._resposta_demo(mensagem)
        except Exception as e:
            logger.error(f"Erro Claude: {e}")
            return self._resposta_demo(mensagem)

    def _chat_gemini(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Chat com Google Gemini"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(mensagem)
            
            resposta = response.text
            self.conversas.append({"usuario": mensagem, "resposta": resposta})
            
            return resposta
        except ImportError:
            return self._resposta_demo(mensagem)
        except Exception as e:
            logger.error(f"Erro Gemini: {e}")
            return self._resposta_demo(mensagem)

    def analisar_sentimento(self, texto: str) -> Dict[str, Any]:
        """Analisa o sentimento de um texto"""
        try:
            from textblob import TextBlob
            
            blob = TextBlob(texto)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentimento = "positivo"
            elif polarity < -0.1:
                sentimento = "negativo"
            else:
                sentimento = "neutro"
            
            return {
                "sentimento": sentimento,
                "confiança": abs(polarity),
                "descricao": f"Sentimento {sentimento} com confiança de {abs(polarity)*100:.1f}%",
                "score": polarity
            }
        except Exception as e:
            logger.warning(f"Erro na análise de sentimento: {e}")
            return {
                "sentimento": "desconhecido",
                "confiança": 0.0,
                "descricao": "Não foi possível analisar",
                "score": 0.0
            }

    def gerar_conteudo(self, tipo: str, tema: str, comprimento: str = "médio") -> str:
        """Gera conteúdo personalizado"""
        prompt = self._construir_prompt_geracao(tipo, tema, comprimento)
        return self.chat(prompt)

    def _construir_prompt_geracao(self, tipo: str, tema: str, comprimento: str) -> str:
        """Constrói prompt para geração de conteúdo"""
        tamanho_map = {
            "curto": "200-300",
            "médio": "500-800",
            "longo": "1500-2000"
        }
        
        tamanho = tamanho_map.get(comprimento, "500-800")
        
        prompts = {
            "artigo": f"Escreva um artigo profissional sobre '{tema}' com {tamanho} palavras.",
            "resumo": f"Faça um resumo conciso sobre '{tema}' com {tamanho} palavras.",
            "poesia": f"Escreva uma poesia criativa sobre '{tema}' com {tamanho} palavras.",
            "código": f"Escreva código Python bem comentado que demonstre '{tema}'.",
            "história": f"Conte uma história criativa sobre '{tema}' com {tamanho} palavras."
        }
        
        return prompts.get(tipo, f"Gere conteúdo sobre '{tema}'")

    def traduzir(self, texto: str, idioma_origem: str = "pt", idioma_destino: str = "en") -> str:
        """Traduz um texto"""
        idiomas = {
            "pt": "Português",
            "en": "Inglês",
            "es": "Espanhol",
            "fr": "Francês",
            "de": "Alemão",
            "ja": "Japonês"
        }
        
        idioma_orig = idiomas.get(idioma_origem, "Português")
        idioma_dest = idiomas.get(idioma_destino, "Inglês")
        
        prompt = f"Traduza o seguinte texto de {idioma_orig} para {idioma_dest}:\\n\\n{texto}\\n\\nApenas forneça a tradução, sem explicações adicionais."
        
        return self.chat(prompt)

    def salvar_memoria(self, chave: str, valor: Any):
        """Salva na memória de AURA"""
        self.memoria[chave] = {
            "valor": valor,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"Memória salva: {chave}")

    def recuperar_memoria(self, chave: str) -> Optional[Any]:
        """Recupera da memória de AURA"""
        if chave in self.memoria:
            return self.memoria[chave]["valor"]
        return None

    def _resposta_demo(self, mensagem: str) -> str:
        """Resposta em modo demonstração"""
        respostas_demo = {
            "oi": "👋 Olá! Sou AURA, seu assistente IA. Como posso ajudá-lo?",
            "como você está": "😊 Estou funcionando perfeitamente! Pronto para ajudar você.",
            "qual é o seu nome": "🌟 Sou AURA - Assistente Inteligente Completo. Prazer em conhecê-lo!",
            "o que você faz": "🤖 Sou um assistente IA avançado que pode: responder perguntas, gerar conteúdo, traduzir, analisar sentimentos e muito mais!",
        }
        
        msg_lower = mensagem.lower()
        for chave, resposta in respostas_demo.items():
            if chave in msg_lower:
                return resposta
        
        return f"✨ Recebi sua mensagem: '{mensagem}'. Configure uma chave de API em .env para respostas completas!"

    def __str__(self) -> str:
        """Representação em string"""
        return f"AURA(provider={self.provider}, model={self.model}, demo_mode={self.demo_mode})"