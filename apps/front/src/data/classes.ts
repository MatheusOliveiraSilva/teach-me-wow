export interface Specialization {
  id: string;
  name: string;
  iconUrl: string; // Placeholder for icon URL
}

export interface WowClass {
  id: string;
  name: string;
  imageUrl: string; // Placeholder for class background image URL
  iconUrl: string; // Placeholder for class icon URL
  specializations: Specialization[];
}

export const wowClasses: WowClass[] = [
  {
    id: 'death-knight',
    name: 'Death Knight',
    imageUrl: '/dk/dk.jpg', // Use class image for background
    iconUrl: '/dk/dk.jpg',   // Use class image for icon (adjust if separate class icon exists)
    specializations: [
      { id: 'blood', name: 'Blood', iconUrl: '/dk/dk_blood.jpg' },
      { id: 'frost', name: 'Frost', iconUrl: '/dk/dk_frost.jpg' },
      { id: 'unholy', name: 'Unholy', iconUrl: '/dk/dk_unh.jpg' }, // Assuming unh for Unholy
    ],
  },
  {
    id: 'demon-hunter',
    name: 'Demon Hunter',
    imageUrl: '/dh/dh.jpg',
    iconUrl: '/dh/dh.jpg',
    specializations: [
      { id: 'havoc', name: 'Havoc', iconUrl: '/dh/dh_havoc.jpg' }, // Assuming convention holds
      { id: 'vengeance', name: 'Vengeance', iconUrl: '/dh/dh_veng.jpg' }, // Assuming convention holds
    ],
  },
  {
    id: 'druid',
    name: 'Druid',
    imageUrl: '/druid/druid.jpg',
    iconUrl: '/druid/druid.jpg',
    specializations: [
      { id: 'balance', name: 'Balance', iconUrl: '/druid/druid_balance.jpg' },
      { id: 'feral', name: 'Feral', iconUrl: '/druid/druid_feral.jpg' },
      { id: 'guardian', name: 'Guardian', iconUrl: '/druid/druid_guardian.jpg' },
      { id: 'restoration', name: 'Restoration', iconUrl: '/druid/druid_resto.jpg' },
    ],
  },
   {
    id: 'evoker',
    name: 'Evoker',
    imageUrl: '/evoker/evoker.jpg',
    iconUrl: '/evoker/evoker.jpg',
    specializations: [
      { id: 'devastation', name: 'Devastation', iconUrl: '/evoker/evoker_deva.jpg' },
      { id: 'preservation', name: 'Preservation', iconUrl: '/evoker/evoker_preserv.jpg' },
      { id: 'augmentation', name: 'Augmentation', iconUrl: '/evoker/evoker_aug.jpg' },
    ],
  },
   {
    id: 'hunter',
    name: 'Hunter',
    imageUrl: '/hunter/hunter.jpg',
    iconUrl: '/hunter/hunter.jpg',
    specializations: [
      { id: 'beast-mastery', name: 'Beast Mastery', iconUrl: '/hunter/hunter_bm.png' }, // Assuming bm for Beast Mastery
      { id: 'marksmanship', name: 'Marksmanship', iconUrl: '/hunter/hunter_mm.jpg' }, // Assuming mm for Marksmanship
      { id: 'survival', name: 'Survival', iconUrl: '/hunter/hunter_surv.jpg' }, // Assuming surv for Survival
    ],
  },
  {
    id: 'mage',
    name: 'Mage',
    imageUrl: '/mage/mage.jpg',
    iconUrl: '/mage/mage.jpg',
    specializations: [
      { id: 'arcane', name: 'Arcane', iconUrl: '/mage/mage_arcane.jpg' },
      { id: 'fire', name: 'Fire', iconUrl: '/mage/mage_fire.jpg' },
      { id: 'frost', name: 'Frost', iconUrl: '/mage/mage_frost.jpg' },
    ],
  },
  // Add other classes here following the same structure
  {
    id: 'monk',
    name: 'Monk',
    imageUrl: '/monk/monk.jpg',
    iconUrl: '/monk/monk.jpg',
    specializations: [
      { id: 'brewmaster', name: 'Brewmaster', iconUrl: '/monk/monk_brew.jpg' },
      { id: 'mistweaver', name: 'Mistweaver', iconUrl: '/monk/monk_mw.jpg' },
      { id: 'windwalker', name: 'Windwalker', iconUrl: '/monk/monk_ww.jpg' },
    ],
  },
  {
    id: '3adin',
    name: 'Paladin',
    imageUrl: '/paladin/pala.jpg', // Assuming pala.jpg exists or needs adding
    iconUrl: '/paladin/pala.jpg',   // Assuming pala.jpg exists or needs adding
    specializations: [
      { id: 'holy', name: 'Holy', iconUrl: '/paladin/pala_holy.jpg' },
      { id: 'protection', name: 'Protection', iconUrl: '/paladin/pala_prot.jpg' },
      { id: 'retribution', name: 'Retribution', iconUrl: '/paladin/pala_retri.jpg' },
    ],
  },
  {
    id: 'priest',
    name: 'Priest',
    imageUrl: '/priest/priest.jpg',
    iconUrl: '/priest/priest.jpg',
    specializations: [
      { id: 'discipline', name: 'Discipline', iconUrl: '/priest/priest_disc.jpg' },
      { id: 'holy', name: 'Holy', iconUrl: '/priest/priest_holy.jpg' },
      { id: 'shadow', name: 'Shadow', iconUrl: '/priest/priest_shadow.jpg' },
    ],
  },
   {
    id: 'rogue',
    name: 'Rogue',
    imageUrl: '/rogue/rogue.jpg',
    iconUrl: '/rogue/rogue.jpg',
    specializations: [
      { id: 'assassination', name: 'Assassination', iconUrl: '/rogue/rogue_assa.jpg' },
      { id: 'outlaw', name: 'Outlaw', iconUrl: '/rogue/rogue_outlaw.jpg' },
      { id: 'subtlety', name: 'Subtlety', iconUrl: '/rogue/rogue_sub.jpg' },
    ],
  },
   {
    id: 'shaman', 
    name: 'Shaman',
    imageUrl: '/shamman/shamman.jpg', 
    iconUrl: '/shamman/shamman.jpg',  
    specializations: [
      { id: 'elemental', name: 'Elemental', iconUrl: '/shamman/shamman_elemental.jpg' },
      { id: 'enhancement', name: 'Enhancement', iconUrl: '/shamman/shamman_enh.jpg' },
      { id: 'restoration', name: 'Restoration', iconUrl: '/shamman/shamman_resto.jpg' },
    ],
  },
  {
    id: 'warlock',
    name: 'Warlock',
    imageUrl: '/warlock/warlock.jpg',
    iconUrl: '/warlock/warlock.jpg',
    specializations: [
      { id: 'affliction', name: 'Affliction', iconUrl: '/warlock/warlock_aff.jpg' },
      { id: 'demonology', name: 'Demonology', iconUrl: '/warlock/warlock_demo.jpg' },
      { id: 'destruction', name: 'Destruction', iconUrl: '/warlock/warlock_destro.jpg' },
    ],
  },
   {
    id: 'warrior', // Using correct name
    name: 'Warrior',
    imageUrl: '/war/warrior.jpg', // Using folder name
    iconUrl: '/war/warrior.jpg',   // Using folder name
    specializations: [
      { id: 'arms', name: 'Arms', iconUrl: '/war/warrior_arms.png' }, 
      { id: 'fury', name: 'Fury', iconUrl: '/war/warrior_fury.jpeg' }, 
      { id: 'protection', name: 'Protection', iconUrl: '/war/warrior_prot.jpg' },
    ],
  },
];

// Helper function to get a class by its ID (slug)
export const getClassById = (id: string): WowClass | undefined => {
  return wowClasses.find(cls => cls.id === id);
};

// Helper function to get a specialization by class ID and spec ID
export const getSpecializationById = (classId: string, specId: string): Specialization | undefined => {
  const wowClass = getClassById(classId);
  return wowClass?.specializations.find(spec => spec.id === specId);
}; 