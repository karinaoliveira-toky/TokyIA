"use client";
import React from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

export default function Login() {
  const router = useRouter();

  const handleLogin = () => {
    router.push('/painel');
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ backgroundColor: '#000000' }}>
      <div
        className="w-full max-w-sm flex flex-col items-center gap-8 p-10 rounded-[20px]"
        style={{
          backgroundColor: '#000000',
          border: '1px solid #2A2E35',
        }}
      >
        {/* Logo */}
        <div className="flex flex-col items-center gap-4">
          <Image
            src="/logo-tokyia.jpg"
            alt="TokyIA Logo"
            width={200}
            height={80}
            className="rounded-lg"
            style={{ objectFit: 'contain' }}
          />
          <p className="text-xs tracking-widest uppercase" style={{ color: '#8B949E' }}>
            Inteligência Corporativa · Grupo Toky
          </p>
        </div>

        {/* Divider */}
        <div className="w-full h-px" style={{ backgroundColor: '#2A2E35' }} />

        {/* Texto */}
        <div className="text-center">
          <h1 className="text-lg font-semibold mb-1" style={{ color: '#E1E4E8' }}>
            Bem-vindo(a) de volta
          </h1>
          <p className="text-sm" style={{ color: '#8B949E' }}>
            Acesse com sua conta corporativa
          </p>
        </div>

        {/* Botão Google */}
        <button
          onClick={handleLogin}
          className="w-full flex items-center justify-center gap-3 py-3 px-5 rounded-full font-medium text-sm transition-all duration-200"
          style={{
            backgroundColor: '#000000',
            border: '1px solid #2A2E35',
            color: '#E1E4E8',
          }}
          onMouseEnter={e => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#2A2E35';
            (e.currentTarget as HTMLButtonElement).style.borderColor = '#4CAF7D';
          }}
          onMouseLeave={e => {
            (e.currentTarget as HTMLButtonElement).style.backgroundColor = '#000000';
            (e.currentTarget as HTMLButtonElement).style.borderColor = '#2A2E35';
          }}
        >
          <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
            <g transform="matrix(1, 0, 0, 1, 27.009001, -39.238998)">
              <path fill="#4285F4" d="M -3.264 51.509 C -3.264 50.719 -3.334 49.969 -3.454 49.239 L -14.754 49.239 L -14.754 53.419 L -8.284 53.419 C -8.554 54.819 -9.414 55.939 -10.534 56.699 L -10.534 59.429 L -6.684 59.429 C -4.464 57.359 -3.264 54.749 -3.264 51.509 Z" />
              <path fill="#34A853" d="M -14.754 63.239 C -11.514 63.239 -8.804 62.159 -6.824 60.429 L -10.534 57.699 C -11.544 58.369 -12.954 58.839 -14.754 58.839 C -18.224 58.839 -21.124 56.529 -22.174 53.369 L -26.104 53.369 L -26.104 56.409 C -24.124 60.309 -19.784 63.239 -14.754 63.239 Z" />
              <path fill="#FBBC05" d="M -22.174 53.369 C -22.464 52.539 -22.614 51.649 -22.614 50.739 C -22.614 49.829 -22.464 48.939 -22.174 48.109 L -22.174 45.069 L -26.104 45.069 C -26.934 46.719 -27.404 48.649 -27.404 50.739 C -27.404 52.829 -26.934 54.759 -26.104 56.409 L -22.174 53.369 Z" />
              <path fill="#EA4335" d="M -14.754 42.679 C -12.924 42.679 -11.334 43.339 -10.084 44.539 L -6.694 41.149 C -8.804 39.169 -11.514 38.139 -14.754 38.139 C -19.784 38.139 -24.124 41.069 -26.104 44.969 L -22.174 48.009 C -21.124 44.849 -18.224 42.679 -14.754 42.679 Z" />
            </g>
          </svg>
          Continuar com o Google
        </button>

        {/* Footer */}
        <p className="text-center text-xs" style={{ color: '#4A5058' }}>
          Ao acessar, você concorda com os{' '}
          <a href="#" className="hover:underline" style={{ color: '#4CAF7D' }}>Termos</a> e{' '}
          <a href="#" className="hover:underline" style={{ color: '#4CAF7D' }}>Política de Privacidade</a>.
        </p>
      </div>
    </div>
  );
}
