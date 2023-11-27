import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

const SearchBar = ({ searchQuery, setSearchQuery }) => {
  return (
    <>
      <label htmlFor="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only">
        Rechercher
      </label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <MagnifyingGlassIcon className="h-6 w-6" aria-hidden="true" />
        </div>
        <input
          type="search"
          id="default-search"
          className="block w-full p-4 pl-14 md:text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-sky-600 focus:border-sky-300"
          placeholder="Rechercher un café"
          autoComplete="off"
          autoCorrect="off"
          spellCheck="false"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
    </>
  );
};

export default SearchBar;
