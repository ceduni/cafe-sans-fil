import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import Container from "./ui/Container";

const Search = () => {
  return (
    <>
      <Container className="py-10">
        <form>
          <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only">
            Rechercher
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <MagnifyingGlassIcon className="h-6 w-6" aria-hidden="true" />
            </div>
            <input
              type="search"
              id="default-search"
              class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-emerald-600 focus:border-emerald-500"
              placeholder="Rechercher un café ou un produit"
              required
            />
            <button
              type="submit"
              class="text-white absolute right-2.5 bottom-2.5 bg-emerald-600 hover:bg-emerald-500 focus:ring-4 focus:outline-none focus:ring-emerald-600 font-medium rounded-lg text-sm px-4 py-2">
              Rechercher
            </button>
          </div>
        </form>
      </Container>
    </>
  );
};

export default Search;
