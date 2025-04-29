import { getClassById, getSpecializationById, wowClasses } from "@/data/classes";
import Link from "next/link";
import Image from "next/image";
import { notFound } from 'next/navigation';

// Define the structure of the params object
interface SpecPageParams {
  classSlug: string;
  specSlug: string;
}

// Generate static paths for all specializations
export async function generateStaticParams(): Promise<SpecPageParams[]> {
  const paths: SpecPageParams[] = [];
  wowClasses.forEach((cls) => {
    cls.specializations.forEach((spec) => {
      paths.push({ classSlug: cls.id, specSlug: spec.id });
    });
  });
  return paths;
}

// Make the component function async
export default async function SpecializationPage({ params }: { params: SpecPageParams }) {
  const { classSlug, specSlug } = params;
  const wowClass = getClassById(classSlug);
  const specialization = getSpecializationById(classSlug, specSlug);

  // If class or spec not found, return 404
  if (!wowClass || !specialization) {
    notFound();
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-4 sm:p-8">
      <div className="max-w-5xl mx-auto">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-400">
          <Link href="/" className="hover:text-yellow-400 transition-colors">Classes</Link>
          <span className="mx-2">/</span>
          <Link href={`/${classSlug}`} className="hover:text-yellow-400 transition-colors">{wowClass.name}</Link>
          <span className="mx-2">/</span>
          <span className="text-white">{specialization.name}</span>
        </div>

        {/* Header */}
        <div className="flex items-center mb-8">
          <div className="flex-shrink-0 w-16 h-16 sm:w-20 sm:h-20 bg-gray-700 rounded-full mr-4 sm:mr-6 border-2 border-gray-600 flex items-center justify-center font-bold text-gray-400">
             {specialization.iconUrl ? (
                <Image src={specialization.iconUrl} alt={`${specialization.name} icon`} width={80} height={80} className="rounded-full object-cover" />
             ) : (
                specialization.name.substring(0, 1).toUpperCase()
             )}
           </div>
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold text-yellow-400">{specialization.name} {wowClass.name}</h1>
            <p className="text-lg text-gray-300">Guide & Builds</p>
          </div>
        </div>

        {/* Placeholder Content */}
        <div className="bg-gray-800/50 p-6 sm:p-8 rounded-lg border border-gray-700 text-center">
          <h2 className="text-2xl font-semibold mb-4">Content Coming Soon!</h2>
          <p className="text-gray-400 mb-6">
            Detailed guides, talent builds, rotation tips, and more for {specialization.name} {wowClass.name} are under construction.
          </p>
          <Link href={`/${classSlug}`} className="inline-block px-6 py-2 bg-yellow-600 text-gray-900 font-semibold rounded hover:bg-yellow-500 transition-colors">
            Back to {wowClass.name} Specializations
          </Link>
        </div>

      </div>
    </main>
  );
} 