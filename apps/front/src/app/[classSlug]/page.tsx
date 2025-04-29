import { getClassById, wowClasses } from "@/data/classes";
import SpecCard from "@/components/SpecCard";
import Image from "next/image";
import Link from "next/link";
import { notFound } from 'next/navigation';

// Define the structure of the params object
interface ClassPageParams {
  classSlug: string;
}

// Generate static paths for all classes
export async function generateStaticParams(): Promise<ClassPageParams[]> {
  return wowClasses.map((cls) => ({ classSlug: cls.id }));
}

// Make the component function async
export default async function ClassPage({ params }: { params: ClassPageParams }) {
  const { classSlug } = params; // Access params within async function
  const wowClass = getClassById(classSlug);

  // If class not found, return 404
  if (!wowClass) {
    notFound();
  }

  // Placeholder texts - replace with actual data later
  const classDescription = `Choose a ${wowClass.name} specialization and learn how to optimally build your character for Solo Shuffle, 2v2, 3v3, Blitz, Rated Battlegrounds, or Mythic+ in The War Within Season 2.`;
  const specDescriptions: { [key: string]: string } = {
    blood: "A dark guardian who manipulates and corrupts life energy to sustain themselves in the face of an enemy onslaught. Preferred Weapon: Two-Handed Axe, Mace, Sword.",
    frost: "An icy harbinger of doom, channeling runic power and delivering vicious weapon strikes. Preferred Weapons: Dual Axes, Maces, Swords.",
    unholy: "A master of death and decay, spreading infection and controlling undead minions to do their bidding. Preferred Weapon: Two-Handed Axe, Mace, Sword.",
    // Add other spec descriptions
  };
    const specWeapons: { [key: string]: string } = {
    blood: "Two-Handed Axe, Mace, Sword",
    frost: "Dual Axes, Maces, Swords",
    unholy: "Two-Handed Axe, Mace, Sword",
    havoc: "Warglaives",
    vengeance: "Warglaives",
    balance: "Staff, Dagger, Mace",
    feral: "Polearm, Staff, Two-Handed Mace",
    guardian: "Polearm, Staff, Two-Handed Mace",
    restoration: "Staff, Dagger, Mace",
    devastation: "Sword, Axe, Mace, Staff",
    preservation: "Sword, Axe, Mace, Staff",
    augmentation: "Sword, Axe, Mace, Staff",
    'beast-mastery': "Bow, Crossbow, Gun",
    marksmanship: "Bow, Crossbow, Gun",
    survival: "Polearm, Staff",
    arcane: "Staff, Wand, Sword, Dagger",
    fire: "Staff, Wand, Sword, Dagger",
    frost_mage: "Staff, Wand, Sword, Dagger", // Use a unique ID if needed
    // Add other spec weapons
  };


  return (
    <main className="min-h-screen bg-gray-950 text-white p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <Link href="/" className="inline-block mb-6 text-yellow-400 hover:text-yellow-300 transition-colors">
          &larr; Back to Classes
        </Link>

        {/* Class Header with Background */}
        <div className="relative rounded-lg overflow-hidden mb-8 sm:mb-12 border border-gray-700">
          <div className="absolute inset-0 z-0 opacity-20" style={{ backgroundImage: `url(${wowClass.imageUrl})`, backgroundSize: 'cover', backgroundPosition: 'center 30%' }}>
             <div className="absolute inset-0 bg-gradient-to-t from-gray-950 via-gray-950/80 to-transparent"></div>
          </div>
           {!wowClass.imageUrl && (
              <div className="absolute inset-0 bg-gradient-to-br from-gray-800/50 to-gray-950/80"></div>
           )}
          <div className="relative z-10 p-6 sm:p-10">
            <h1 className="text-4xl sm:text-5xl font-bold mb-4 text-yellow-400 drop-shadow-lg">{wowClass.name}</h1>
            <p className="text-lg text-gray-300 max-w-3xl">{classDescription}</p>
          </div>
        </div>


        {/* Specialization Grid */}
        <h2 className="text-2xl sm:text-3xl font-semibold mb-6 text-center sm:text-left">Choose a Specialization</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {wowClass.specializations.map((spec) => (
            <SpecCard
              key={spec.id}
              spec={spec}
              classId={wowClass.id}
              description={specDescriptions[spec.id]} // Pass specific description
              preferredWeapons={specWeapons[spec.id]}
            />
          ))}
        </div>
      </div>
    </main>
  );
} 