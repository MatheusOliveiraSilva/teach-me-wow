"use client";

import Link from 'next/link';
import Image from 'next/image';
import { WowClass } from '@/data/classes';

interface ClassCardProps {
  wowClass: WowClass;
}

export default function ClassCard({ wowClass }: ClassCardProps) {
  return (
    <Link href={`/${wowClass.id}`} className="block group relative rounded-lg overflow-hidden shadow-lg bg-gray-900 hover:scale-[1.03] transition-transform duration-300 ease-in-out border border-gray-700 hover:border-yellow-500">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
         {wowClass.imageUrl ? (
            <Image
              src={wowClass.imageUrl}
              alt={`${wowClass.name} background`}
              layout="fill"
              objectFit="cover"
              className="opacity-30 group-hover:opacity-50 transition-opacity duration-300"
              unoptimized
            />
         ) : (
           <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-950 opacity-80 group-hover:opacity-100 transition-opacity"></div>
         )}
         <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/80 to-transparent"></div> {/* Gradient Overlay */}
      </div>

      <div className="relative z-10 p-5 min-h-[160px] flex flex-col justify-between text-white">
        {/* Top Section: Icon and Name */}
        <div className="flex items-center mb-4">
          {/* Class Icon */}
           <div className="flex-shrink-0 w-14 h-14 sm:w-16 sm:h-16 bg-gray-700 rounded-full mr-3 sm:mr-4 border-2 border-gray-600 flex items-center justify-center font-bold text-gray-400 overflow-hidden">
             {wowClass.iconUrl ? (
                <Image
                  src={wowClass.iconUrl}
                  alt={`${wowClass.name} icon`}
                  width={64}
                  height={64}
                  className="object-cover"
                  unoptimized
                />
             ) : (
                wowClass.name.substring(0, 2).toUpperCase()
             )}
           </div>
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight group-hover:text-yellow-400 transition-colors duration-200">{wowClass.name}</h2>
        </div>

        {/* Bottom Section: Specializations */}
        <div className="flex flex-wrap gap-x-3 gap-y-2 mt-auto">
          {wowClass.specializations.map((spec) => (
            <Link
              key={spec.id}
              href={`/${wowClass.id}/${spec.id}`}
              onClick={(e) => e.stopPropagation()} // Prevent card click when clicking spec link
              className="flex items-center space-x-1.5 px-2.5 py-1 bg-black/50 hover:bg-yellow-600/80 border border-gray-600 hover:border-yellow-500 rounded-md transition-all duration-200 text-xs sm:text-sm z-20 group/spec"
            >
              {/* Spec Icon */}
               <div className="flex-shrink-0 w-4 h-4 sm:w-5 sm:h-5 bg-gray-600 rounded-full flex items-center justify-center text-[10px] sm:text-xs font-semibold group-hover/spec:scale-110 transition-transform overflow-hidden">
                 {spec.iconUrl ? (
                     <Image
                       src={spec.iconUrl}
                       alt={`${spec.name} icon`}
                       width={20}
                       height={20}
                       className="object-cover"
                       unoptimized
                     />
                 ) : (
                    spec.name.substring(0, 1).toUpperCase()
                 )}
               </div>
              <span className="group-hover/spec:text-white transition-colors">{spec.name}</span>
            </Link>
          ))}
        </div>
      </div>
    </Link>
  );
} 