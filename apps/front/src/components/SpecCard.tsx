"use client";

import Link from 'next/link';
import Image from 'next/image';
import { Specialization } from '@/data/classes';

interface SpecCardProps {
  spec: Specialization;
  classId: string;
  // Adding placeholder description and preferred weapons (optional)
  description?: string;
  preferredWeapons?: string;
}

export default function SpecCard({ spec, classId, description, preferredWeapons }: SpecCardProps) {
  const defaultDescription = "Choose this specialization to learn how to optimally build your character for Solo Shuffle, 2v2, 3v3, Blitz, Rated Battlegrounds, or Mythic+ in The War Within Season 2.";

  return (
    <Link href={`/${classId}/${spec.id}`} className="block group relative rounded-lg overflow-hidden shadow-lg bg-gray-800/70 hover:bg-gray-700/90 border border-gray-700 hover:border-yellow-500 transition-all duration-200 ease-in-out p-4 sm:p-6 text-white min-h-[180px] flex flex-col">
      <div className="flex items-center mb-3">
        {/* Spec Icon */}
        <div className="flex-shrink-0 w-12 h-12 sm:w-16 sm:h-16 bg-gray-700 rounded-full mr-3 sm:mr-4 border-2 border-gray-600 flex items-center justify-center font-bold text-gray-400 group-hover:scale-105 transition-transform overflow-hidden">
           {spec.iconUrl ? (
              <Image
                src={spec.iconUrl}
                alt={`${spec.name} icon`}
                width={64}
                height={64}
                className="object-cover"
                unoptimized
              />
           ) : (
              spec.name.substring(0, 1).toUpperCase()
           )}
        </div>
        <h3 className="text-lg sm:text-xl font-semibold group-hover:text-yellow-400 transition-colors">{spec.name}</h3>
      </div>
      <p className="text-sm text-gray-300 line-clamp-3 mb-2 flex-grow">
        {description || defaultDescription}
      </p>
      {preferredWeapons && (
        <p className="text-xs text-gray-400 mt-auto">
          <span className="font-semibold">Preferred Weapons:</span> {preferredWeapons}
        </p>
      )}
    </Link>
  );
} 