import ClassCard from "@/components/ClassCard";
import { wowClasses } from "@/data/classes";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-950 text-white p-4 sm:p-8">
      <h1 className="text-3xl sm:text-4xl font-bold text-center mb-8 sm:mb-12 text-yellow-400">Choose Your Class</h1>
      <div className="flex flex-wrap justify-center gap-6 sm:gap-8 max-w-7xl mx-auto">
        {wowClasses.map((wowClass) => (
          <ClassCard key={wowClass.id} wowClass={wowClass} />
        ))}
      </div>
    </main>
  );
}
