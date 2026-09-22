"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Send, BarChart3, Package, Truck, Sparkles, ArrowRight, MessageSquare, LogOut } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

export default function Painel() {
  const router = useRouter();
  const [input, setInput] = useState('');

  const irParaChat = (textoPronto = "") => {
    const perguntaFinal = textoPronto || input;
    if (perguntaFinal.trim()) {
      router.push(`/chat?q=${encodeURIComponent(perguntaFinal)}`);
    } else {
      router.push('/chat');
    }
  };

  const sugestoes = [
    {
      titulo: "Vendas & GMV",
      descricao: "Faturamento total da Tok&Stok no último mês",
      icone: <BarChart3 size={16} style={{ color: '#4CAF7D' }} />,
      query: "Qual o faturamento total e vendas da Tok&Stok no último mês?"
    },
    {
      titulo: "Estoque & Ruptura",
      descricao: "SKUs com maior risco de ruptura na Mobly",
      icone: <Package size={16} style={{ color: '#4CAF7D' }} />,
      query: "Quais são os SKUs de maior estoque e risco de ruptura na Mobly?"
    },
    {
      titulo: "Logística & SLA",
      descricao: "Tempo médio de entrega e atrasos da Guldi",
      icone: <Truck size={16} style={{ color: '#4CAF7D' }} />,
      query: "Qual o SLA médio de entrega e frete dos pedidos da Guldi?"
    },
    {
      titulo: "Desempenho vs Meta",
      descricao: "Vendas realizadas comparadas às metas do grupo",
      icone: <Sparkles size={16} style={{ color: '#4CAF7D' }} />,
      query: "Como está o desempenho das vendas comparado às metas?"
    }
  ];

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: '#000000' }}>
      {/* Header */}
      <header
        className="flex items-center justify-between px-6 py-3 shrink-0"
        style={{ borderBottom: '1px solid #2A2E35', backgroundColor: '#000000' }}
      >
        <Image
          src="/logo-tokyia.jpg"
          alt="TokyIA"
          width={120}
          height={40}
          style={{ objectFit: 'contain' }}
          className="rounded"
        />

        <div className="flex items-center gap-2">
          <Link
            href="/painel"
            className="text-xs font-medium px-3 py-1.5 rounded-full"
            style={{ backgroundColor: '#000000', color: '#4CAF7D', border: '1px solid #4CAF7D33' }}
          >
            Painel
          </Link>
          <Link
            href="/chat"
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full transition-all"
            style={{ color: '#8B949E', border: '1px solid #2A2E35' }}
            onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.color = '#E1E4E8'}
            onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.color = '#8B949E'}
          >
            <MessageSquare size={13} />
            Chat IA
          </Link>
          <Link
            href="/"
            className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-full transition-all"
            style={{ color: '#4A5058' }}
            onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.color = '#E1E4E8'}
            onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.color = '#4A5058'}
          >
            <LogOut size={13} />
            Sair
          </Link>
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 gap-10">
        {/* Headline */}
        <div className="text-center max-w-xl">
          <div
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs mb-5"
            style={{ backgroundColor: '#000000', color: '#8B949E', border: '1px solid #2A2E35' }}
          >
            <Sparkles size={12} style={{ color: '#4CAF7D' }} />
            Chefe de Gabinete Estratégico · Grupo Toky
          </div>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight mb-3" style={{ color: '#E1E4E8' }}>
            O que vamos analisar hoje?
          </h1>
          <p className="text-sm" style={{ color: '#8B949E' }}>
            Acesse métricas de Tok&Stok, Mobly e Guldi via Text-to-SQL em tempo real.
          </p>
        </div>

        {/* Input */}
        <div className="w-full max-w-2xl">
          <div
            className="flex items-center gap-3 px-5 py-3 rounded-full"
            style={{
              backgroundColor: '#000000',
              border: '1px solid #2A2E35',
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && irParaChat()}
              placeholder="Pergunte sobre vendas, estoque, SLA ou metas..."
              className="flex-1 bg-transparent outline-none text-sm"
              style={{ color: '#E1E4E8' }}
            />
            <button
              onClick={() => irParaChat()}
              className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 transition-all"
              style={{ backgroundColor: '#4CAF7D' }}
              onMouseEnter={e => (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#5DBF8E'}
              onMouseLeave={e => (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#4CAF7D'}
            >
              <Send size={14} color="#000000" />
            </button>
          </div>
        </div>

        {/* Cards de sugestão */}
        <div className="w-full max-w-2xl grid grid-cols-1 sm:grid-cols-2 gap-3">
          {sugestoes.map((s, i) => (
            <button
              key={i}
              onClick={() => irParaChat(s.query)}
              className="group flex items-start justify-between p-4 rounded-[16px] text-left transition-all duration-200"
              style={{
                backgroundColor: '#000000',
                border: '1px solid #2A2E35',
              }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLButtonElement).style.borderColor = '#4CAF7D44';
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#000000';
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLButtonElement).style.borderColor = '#2A2E35';
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#000000';
              }}
            >
              <div className="flex flex-col gap-1">
                <div className="flex items-center gap-2 text-sm font-medium" style={{ color: '#E1E4E8' }}>
                  {s.icone}
                  {s.titulo}
                </div>
                <p className="text-xs" style={{ color: '#8B949E' }}>{s.descricao}</p>
              </div>
              <ArrowRight size={14} style={{ color: '#4A5058', marginTop: '2px', flexShrink: 0 }} />
            </button>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs py-4" style={{ color: '#4A5058' }}>
        TokyIA © 2026 · Grupo Toky
      </footer>
    </div>
  );
}
