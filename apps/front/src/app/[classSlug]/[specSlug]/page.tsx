// Esta página é agora um Server Component por padrão
import React from 'react';
import { getClassById, getSpecializationById, wowClasses } from "@/data/classes";
import { notFound } from 'next/navigation';
import SpecializationChatPageContent from './SpecializationChatPageContent'; // Importar o novo client component

// Define the structure of the params object
interface SpecPageParams {
  classSlug: string;
  specSlug: string;
}

// Generate static paths for all specializations
// Esta função SÓ PODE existir em Server Components
export async function generateStaticParams(): Promise<SpecPageParams[]> {
  const paths: SpecPageParams[] = [];
  wowClasses.forEach((cls) => {
    cls.specializations.forEach((spec) => {
      paths.push({ classSlug: cls.id, specSlug: spec.id });
    });
  });
  return paths;
}

// Opcional: Função generateMetadata para metadados da página (Server Component feature)
export async function generateMetadata({ params }: { params: SpecPageParams }) {
  const wowClass = getClassById(params.classSlug);
  const specialization = getSpecializationById(params.classSlug, params.specSlug);
  
  if (!wowClass || !specialization) {
    return {
      title: "Especialização não encontrada",
    };
  }
  return {
    title: `${specialization.name} ${wowClass.name} Guide & Chat - TeachMeWow`,
    description: `Converse com o Mestre do Conhecimento e aprenda a jogar de ${specialization.name} ${wowClass.name}.`,
  };
}

// Este é o Server Component da página
const SpecializationPage = ({ params }: { params: SpecPageParams }) => {
  const { classSlug, specSlug } = params;

  // Validação de dados pode ocorrer aqui (Server-Side)
  const wowClass = getClassById(classSlug);
  const specialization = getSpecializationById(classSlug, specSlug);

  if (!wowClass || !specialization) {
    notFound(); // Função notFound do Next.js para retornar 404 (Server-Side)
  }

  // Renderiza o Client Component que contém a lógica interativa
  return <SpecializationChatPageContent />;
};

export default SpecializationPage; 