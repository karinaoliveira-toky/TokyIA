"use client";
import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Plus, Loader2, FileText, FileSpreadsheet, Database, Sparkles, LogOut, Paperclip } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Link from 'next/link';
import Image from 'next/image';

// =====================================================================
// Tipos
// =====================================================================
interface Fonte {
  titulo: string;
  tipo: string;
  url_simulada: string;
  relevancia: number;
  conteudo?: string;
}

interface Message {
  id?: string;
  role: 'ia' | 'user';
  text: string;
  fontes?: Fonte[];
  feedback?: 'positivo' | 'negativo';
}

// =====================================================================
// Componente: Badge de Fonte — estilo pill dark discreto
// =====================================================================
function FonteBadge({ fonte }: { fonte: Fonte; index: number }) {
  const getIcon = () => {
    if (fonte.tipo === 'PDF')      return <FileText size={11} />;
    if (fonte.tipo === 'Planilha') return <FileSpreadsheet size={11} />;
    if (fonte.tipo === 'SQL' || fonte.tipo === 'Database') return <Database size={11} />;
    return <FileText size={11} />;
  };

  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs transition-all"
        style={{
          backgroundColor: '#000000',
          border: '1px solid #2A2E35',
          color: '#8B949E',
        }}
        onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.borderColor = '#4CAF7D44'}
        onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.borderColor = '#2A2E35'}
      >
        <span style={{ color: '#4CAF7D' }}>{getIcon()}</span>
        <span style={{ color: '#8B949E' }}>{fonte.titulo}</span>
        <span
          className="text-[9px] px-1.5 py-0.5 rounded-full uppercase font-medium"
          style={{ backgroundColor: '#2A2E35', color: '#4A5058' }}
        >
          {fonte.tipo}
        </span>
      </button>

      {/* SQL expandido */}
      {open && fonte.conteudo && (
        <div
          className="absolute bottom-full mb-2 left-0 z-50 p-3 rounded-xl text-xs font-mono max-w-sm overflow-x-auto"
          style={{
            backgroundColor: '#000000',
            border: '1px solid #2A2E35',
            color: '#E1E4E8',
            minWidth: '280px',
          }}
        >
          <pre className="whitespace-pre-wrap">{fonte.conteudo}</pre>
        </div>
      )}
    </div>
  );
}

function FontesSection({ fontes }: { fontes: Fonte[] }) {
  if (!fontes || fontes.length === 0) return null;
  return (
    <div className="mt-2 flex flex-wrap gap-1.5 items-center">
      <div className="flex items-center gap-1 mr-1">
        <Sparkles size={10} style={{ color: '#4CAF7D' }} />
        <span className="text-[10px] uppercase tracking-wider" style={{ color: '#4A5058' }}>Fonte</span>
      </div>
      {fontes.map((fonte, idx) => (
        <FonteBadge key={idx} fonte={fonte} index={idx} />
      ))}
    </div>
  );
}

// =====================================================================
// Página Principal do Chat
// =====================================================================
export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome-msg',
      role: 'ia',
      text: 'Olá! Sou a **TokyIA**, sua inteligência corporativa.\n\nJá carreguei os dados da **Tok&Stok**, **Mobly** e **Guldi**. Posso analisar vendas, estoque, logística, mensagens de atendimento e muito mais.\n\nO que vamos analisar hoje?',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => { scrollToBottom(); }, [messages, isLoading]);

  const sendMessage = async (userMsg: string) => {
    if (!userMsg.trim()) return;

    const userMsgId = `msg-usr-${Date.now()}`;
    const iaMsgId   = `msg-ia-${Date.now()}`;

    setMessages(prev => [...prev, { id: userMsgId, role: 'user', text: userMsg }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem: userMsg }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessages(prev => [...prev, {
          id: iaMsgId,
          role: 'ia',
          text: data.resposta,
          fontes: data.fontes ?? [],
        }]);
      } else {
        setMessages(prev => [...prev, {
          id: iaMsgId,
          role: 'ia',
          text: '⚠️ Erro no servidor. Verifique o terminal do Python.',
        }]);
      }
    } catch {
      setMessages(prev => [...prev, {
        id: iaMsgId,
        role: 'ia',
        text: '🔌 Não foi possível conectar ao backend. O servidor está rodando na porta **8000**?',
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    const msg = input.trim();
    setInput('');
    sendMessage(msg);
  };

  const hasSentInitialQuery = useRef(false);
  useEffect(() => {
    if (hasSentInitialQuery.current) return;
    hasSentInitialQuery.current = true;
    const urlParams = new URLSearchParams(window.location.search);
    const q = urlParams.get('q');
    if (q) {
      window.history.replaceState({}, '', '/chat');
      sendMessage(q);
    }
  }, []);

  const handleFeedback = async (mensagemId: string, tipo: 'positivo' | 'negativo', respostaIa: string) => {
    let promptUsuario = '';
    const idx = messages.findIndex(m => m.id === mensagemId);
    if (idx > 0 && messages[idx - 1].role === 'user') {
      promptUsuario = messages[idx - 1].text;
    }
    setMessages(prev => prev.map(m => m.id === mensagemId ? { ...m, feedback: tipo } : m));
    try {
      await fetch('http://localhost:8000/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem_id: mensagemId, prompt_usuario: promptUsuario, resposta_ia: respostaIa, feedback: tipo }),
      });
    } catch {}
  };

  const novaAnalise = () => {
    setMessages([{ id: 'welcome-msg', role: 'ia', text: 'Nova sessão iniciada. Como posso ajudar?' }]);
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  // histórico de sessão (mockado — últimas 3 mensagens do user)
  const historico = messages.filter(m => m.role === 'user').slice(-5).reverse();

  return (
    <div className="h-screen flex overflow-hidden" style={{ backgroundColor: '#000000' }}>

      {/* ================================================================
          SIDEBAR
      ================================================================ */}
      <aside
        className="w-60 flex-col hidden md:flex shrink-0"
        style={{
          backgroundColor: '#000000',
          borderRight: '1px solid #2A2E35',
        }}
      >
        {/* Logo */}
        <div className="px-4 pt-5 pb-4" style={{ borderBottom: '1px solid #2A2E35' }}>
          <Image
            src="/logo-tokyia.jpg"
            alt="TokyIA"
            width={140}
            height={46}
            style={{ objectFit: 'contain', width: '100%', height: 'auto' }}
            className="rounded"
          />
        </div>

        {/* Nova Análise */}
        <div className="px-3 py-3">
          <button
            onClick={novaAnalise}
            className="w-full flex items-center gap-2 py-2 px-3 rounded-full text-sm font-medium transition-all"
            style={{
              border: '1px solid #4CAF7D55',
              color: '#4CAF7D',
              backgroundColor: 'transparent',
            }}
            onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#4CAF7D11'}
            onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'transparent'}
          >
            <Plus size={14} />
            Nova Análise
          </button>
        </div>

        {/* Histórico */}
        <div className="flex-1 overflow-y-auto px-3 py-2">
          <p className="text-[10px] uppercase tracking-widest mb-2 px-1" style={{ color: '#4A5058' }}>
            Histórico
          </p>
          {historico.length === 0 ? (
            <p className="text-xs px-1 italic" style={{ color: '#4A5058' }}>
              Nenhuma análise ainda.
            </p>
          ) : (
            historico.map((m, i) => (
              <button
                key={i}
                onClick={() => sendMessage(m.text)}
                className="w-full text-left text-xs py-2 px-2 rounded-lg mb-1 truncate transition-all"
                style={{ color: '#8B949E' }}
                onMouseEnter={e => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#000000';
                  (e.currentTarget as HTMLButtonElement).style.color = '#E1E4E8';
                }}
                onMouseLeave={e => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'transparent';
                  (e.currentTarget as HTMLButtonElement).style.color = '#8B949E';
                }}
              >
                {m.text}
              </button>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="px-3 py-3" style={{ borderTop: '1px solid #2A2E35' }}>
          <Link
            href="/"
            className="flex items-center gap-2 text-xs py-2 px-2 rounded-lg transition-all"
            style={{ color: '#4A5058' }}
            onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.color = '#8B949E'}
            onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.color = '#4A5058'}
          >
            <LogOut size={13} />
            Sair
          </Link>
        </div>
      </aside>

      {/* ================================================================
          ÁREA PRINCIPAL
      ================================================================ */}
      <main className="flex-1 flex flex-col overflow-hidden">

        {/* Header mobile com logo */}
        <header
          className="flex items-center justify-between px-4 py-3 md:hidden shrink-0"
          style={{ borderBottom: '1px solid #2A2E35', backgroundColor: '#000000' }}
        >
          <Image src="/logo-tokyia.jpg" alt="TokyIA" width={100} height={34} style={{ objectFit: 'contain' }} className="rounded" />
          <Link href="/" style={{ color: '#4A5058' }}>
            <LogOut size={16} />
          </Link>
        </header>

        {/* Container do chat */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-4 py-6 flex flex-col gap-5">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex flex-col gap-1.5 max-w-[80%]">
                  {/* Balão */}
                  <div
                    className="px-4 py-3 rounded-[18px] text-sm leading-relaxed"
                    style={
                      msg.role === 'user'
                        ? {
                            backgroundColor: '#ECEBE4',
                            color: '#000000',
                            borderBottomRightRadius: '4px',
                          }
                        : {
                            backgroundColor: '#0F0F0F',
                            color: '#E1E4E8',
                            border: '1px solid #2A2E35',
                            borderBottomLeftRadius: '4px',
                          }
                    }
                  >
                    {msg.role === 'user' ? (
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    ) : (
                      <div className="prose max-w-none text-sm leading-relaxed" style={{ color: '#E1E4E8' }}>
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                            strong: ({ children }) => <strong style={{ color: '#E1E4E8', fontWeight: 600 }}>{children}</strong>,
                            ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                            ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                            li: ({ children }) => <li style={{ color: '#C9D1D9' }}>{children}</li>,
                            h1: ({ children }) => <h1 className="text-base font-bold mb-2 mt-3" style={{ color: '#E1E4E8' }}>{children}</h1>,
                            h2: ({ children }) => <h2 className="text-sm font-bold mb-1 mt-2" style={{ color: '#E1E4E8' }}>{children}</h2>,
                            h3: ({ children }) => <h3 className="text-sm font-semibold mb-1 mt-2" style={{ color: '#E1E4E8' }}>{children}</h3>,
                            blockquote: ({ children }) => (
                              <blockquote className="pl-3 py-1 italic my-2 rounded" style={{ borderLeft: '3px solid #4CAF7D55', color: '#8B949E', backgroundColor: '#000000' }}>
                                {children}
                              </blockquote>
                            ),
                            code: ({ children }) => (
                              <code className="px-1.5 py-0.5 rounded text-xs font-mono" style={{ backgroundColor: '#000000', color: '#4CAF7D' }}>
                                {children}
                              </code>
                            ),
                            pre: ({ children }) => (
                              <pre className="p-3 rounded-xl my-2 overflow-x-auto text-xs font-mono" style={{ backgroundColor: '#000000', border: '1px solid #2A2E35', color: '#E1E4E8' }}>
                                {children}
                              </pre>
                            ),
                            table: ({ children }) => (
                              <div className="overflow-x-auto my-3 rounded-xl" style={{ border: '1px solid #2A2E35' }}>
                                <table className="min-w-full text-xs">{children}</table>
                              </div>
                            ),
                            thead: ({ children }) => <thead style={{ backgroundColor: '#000000' }}>{children}</thead>,
                            tbody: ({ children }) => <tbody>{children}</tbody>,
                            tr: ({ children }) => <tr style={{ borderBottom: '1px solid #2A2E35' }}>{children}</tr>,
                            th: ({ children }) => <th className="px-3 py-2 text-left font-semibold uppercase text-[10px] tracking-wider" style={{ color: '#8B949E' }}>{children}</th>,
                            td: ({ children }) => <td className="px-3 py-2" style={{ color: '#C9D1D9' }}>{children}</td>,
                          }}
                        >
                          {msg.text}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>

                  {/* Feedback — chips discretos */}
                  {msg.role === 'ia' && msg.id && msg.id !== 'welcome-msg' && (
                    <div className="flex items-center gap-2 ml-1">
                      {(['positivo', 'negativo'] as const).map(tipo => (
                        <button
                          key={tipo}
                          onClick={() => handleFeedback(msg.id!, tipo, msg.text)}
                          className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] transition-all"
                          style={{
                            backgroundColor: msg.feedback === tipo
                              ? tipo === 'positivo' ? '#4CAF7D22' : '#EF444422'
                              : '#000000',
                            border: `1px solid ${
                              msg.feedback === tipo
                                ? tipo === 'positivo' ? '#4CAF7D55' : '#EF444455'
                                : '#2A2E35'
                            }`,
                            color: msg.feedback === tipo
                              ? tipo === 'positivo' ? '#4CAF7D' : '#EF4444'
                              : '#4A5058',
                          }}
                        >
                          {tipo === 'positivo' ? '👍' : '👎'}
                          <span>{tipo === 'positivo' ? 'Útil' : 'Não útil'}</span>
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Fontes */}
                  {msg.role === 'ia' && msg.fontes && msg.fontes.length > 0 && (
                    <FontesSection fontes={msg.fontes} />
                  )}
                </div>
              </div>
            ))}

            {/* Loading */}
            {isLoading && (
              <div className="flex justify-start">
                <div
                  className="flex items-center gap-2 px-4 py-3 rounded-[18px] text-sm"
                  style={{
                    backgroundColor: '#000000',
                    border: '1px solid #2A2E35',
                    color: '#8B949E',
                    borderBottomLeftRadius: '4px',
                  }}
                >
                  <Loader2 size={13} className="animate-spin" style={{ color: '#4CAF7D' }} />
                  <span className="text-xs">Consultando o Databricks...</span>
                  <div className="flex gap-1 ml-1">
                    {[0, 1, 2].map(i => (
                      <div
                        key={i}
                        className="w-1 h-1 rounded-full animate-bounce"
                        style={{ backgroundColor: '#4CAF7D', animationDelay: `${i * 150}ms` }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* ============================================================
            INPUT BAR — Pill flutuante na base
        ============================================================ */}
        <div className="px-4 pb-5 pt-3 shrink-0" style={{ backgroundColor: '#000000' }}>
          <div className="max-w-3xl mx-auto">
            <div
              className="flex items-center gap-3 px-5 py-3 rounded-full transition-all"
              style={{
                backgroundColor: '#000000',
                border: '1px solid #2A2E35',
              }}
              onFocusCapture={e => (e.currentTarget as HTMLDivElement).style.borderColor = '#4CAF7D44'}
              onBlurCapture={e => (e.currentTarget as HTMLDivElement).style.borderColor = '#2A2E35'}
            >
              {/* Ícone de anexo */}
              <button
                className="shrink-0 transition-colors"
                style={{ color: '#4A5058' }}
                onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = '#8B949E'}
                onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = '#4A5058'}
              >
                <Paperclip size={15} />
              </button>

              {/* Campo de texto */}
              <input
                ref={inputRef as unknown as React.RefObject<HTMLInputElement>}
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
                placeholder="Pergunte sobre vendas, estoque, atendimento..."
                disabled={isLoading}
                className="flex-1 bg-transparent outline-none text-sm"
                style={{ color: '#E1E4E8' }}
              />

              {/* Mic */}
              <button
                className="shrink-0 transition-colors"
                style={{ color: '#4A5058' }}
                onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.color = '#8B949E'}
                onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.color = '#4A5058'}
              >
                <Mic size={15} />
              </button>

              {/* Enviar */}
              <button
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 transition-all disabled:opacity-40"
                style={{ backgroundColor: '#4CAF7D' }}
                onMouseEnter={e => !isLoading && input.trim() && ((e.currentTarget as HTMLButtonElement).style.backgroundColor = '#5DBF8E')}
                onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#4CAF7D'}
              >
                <Send size={13} color="#000000" />
              </button>
            </div>

            <p className="text-center text-[10px] mt-2" style={{ color: '#4A5058' }}>
              Apenas consultas SELECT são executadas no Databricks · Grupo Toky © 2026
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
