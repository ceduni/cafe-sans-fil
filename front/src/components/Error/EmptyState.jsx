import { FolderOpenIcon, XCircleIcon } from "@heroicons/react/24/outline";

const EmptyState = ({ type = "empty", name = "élément", genre = "masculin", error }) => {
  return (
    <div className="flex flex-col items-center justify-center py-10">
      {type === "empty" && (
        <>
          <FolderOpenIcon className="h-12 w-12 text-gray-400" />
          <p className="mt-6 leading-7 text-gray-600 font-semibold">
            {genre === "masculin" ? "Aucun" : "Aucune"} {name} n'a été {genre === "masculin" ? "trouvé" : "trouvée"}
          </p>
        </>
      )}
      {type === "error" && (
        <>
          <XCircleIcon className="h-12 w-12 text-gray-400" />
          <p className="mt-6 leading-7 text-gray-600 font-semibold">Une erreur est survenue</p>
          <p className="leading-7 text-gray-600">
            {!error.status ? "L'API est-elle bien lancée?" : `${error.status}: ${error.statusText || error.message}`}
          </p>
        </>
      )}
    </div>
  );
};

export default EmptyState;
