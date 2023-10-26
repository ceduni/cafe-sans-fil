import { FolderOpenIcon } from "@heroicons/react/24/outline";

const EmptyState = ({ itemName = "élément", icon: Icon = FolderOpenIcon }) => {
  return (
    <div className="flex flex-col items-center justify-center py-10">
      <Icon className="h-12 w-12 text-gray-400" />
      <p className="mt-6 text-base leading-7 text-gray-600 text-center">Aucun {itemName} n'a été trouvé.</p>
    </div>
  );
};

export default EmptyState;
