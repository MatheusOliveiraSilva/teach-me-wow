'use client';

import React from 'react';
import ChatInterface from '@/components/ChatInterface';
import { useParams, notFound } from 'next/navigation';
import { getClassById, getSpecializationById } from "@/data/classes"; // Assumindo que esta função não precisa de ambiente de servidor
import Link from 'next/link';
import Image from 'next/image';

const SpecializationChatPageContent: React.FC = () => {
  const params = useParams();
  
  const classSlug = (
    Array.isArray(params.classSlug) 
      ? params.classSlug.join('/') 
      : params.classSlug
  ) || '';
  
  const specSlug = (
    Array.isArray(params.specSlug) 
      ? params.specSlug.join('/') 
      : params.specSlug
  ) || '';

  // As funções getClassById e getSpecializationById são chamadas aqui.
  // Se elas fizerem chamadas de API ou acesso a DB, devem ser passadas como props
  // ou a lógica de data fetching deve ocorrer no Server Component pai.
  // Para este exemplo, vamos assumir que são funções síncronas puras baseadas em @/data/classes.
  const wowClass = getClassById(classSlug);
  const specialization = getSpecializationById(classSlug, specSlug);

  if (!wowClass || !specialization) {
    // notFound() idealmente é chamado do Server Component pai.
    // Em um client component, você pode renderizar uma mensagem de não encontrado
    // ou redirecionar, mas notFound() de next/navigation pode não funcionar como esperado aqui.
    // Para manter simples, renderizaremos uma mensagem, mas o ideal é tratar no server component.
    return (
        <div className="flex flex-col items-center justify-center h-full bg-gray-900 text-white text-center p-4">
            <h1 className="text-3xl font-bold">Especialização não encontrada</h1>
            <p className="text-lg text-gray-400 mt-4">Não foi possível encontrar dados para {classSlug}/{specSlug}.</p>
            <Link href="/" className="mt-6 inline-block px-6 py-2 bg-yellow-600 text-gray-900 font-semibold rounded hover:bg-yellow-500 transition-colors">
                Voltar para Classes
            </Link>
        </div>
    );
  }

  const specializationName = specialization.name;
  const className = wowClass.name;

  // O ChatInterface agora efetivamente se torna o layout principal desta rota.
  // O header foi removido daqui e pode ser integrado ao ChatInterface ou a um layout superior se necessário.
  return (
    // Container principal que ocupa a altura total e organiza em coluna
    <div className="flex flex-col h-full w-full bg-gray-900 text-white">
      {/* Cabeçalho com padding e borda inferior */}
      <header className="px-4 md:px-6 py-4 border-b border-gray-700 flex-shrink-0">
        {/* Breadcrumbs */}
        <nav className="text-sm mb-2 text-gray-400">
          <Link href="/" className="hover:text-yellow-400 transition-colors">Classes</Link> 
          / <Link href={`/${classSlug}`} className="hover:text-yellow-400 transition-colors capitalize">{className}</Link> 
          / <span className="capitalize font-semibold text-yellow-400">{specializationName}</span>
        </nav>
        {/* Ícone, Título e Descrição */}
        <div className="flex items-center">
            {specialization.iconUrl && (
                <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-gray-700 rounded-full mr-3 sm:mr-4 border-2 border-gray-600 flex items-center justify-center">
                    <Image src={specialization.iconUrl} alt={`${specialization.name} icon`} width={64} height={64} className="rounded-full object-cover" />
                </div>
            )}
            <div>
                <h1 className="text-2xl md:text-3xl font-bold text-yellow-400">
                {specializationName} <span className="text-white">{className}</span>
                </h1>
                <p className="text-sm md:text-base text-gray-300">
                Converse com o Mestre do Conhecimento sobre {specializationName} {className}.
                </p>
            </div>
        </div>
      </header>
      
      {/* Área principal que contém o chat e ocupa o espaço restante */}
      <main className="flex-grow overflow-hidden">
        {/* O ChatInterface agora está dentro de um 'main' que cresce */}
        <ChatInterface specIconUrl={specialization.iconUrl} />
      </main>
    </div>
  );
};

export default SpecializationChatPageContent; 