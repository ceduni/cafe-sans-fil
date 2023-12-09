import EmptyState from "@/components/EmptyState";
import { CafeCard } from "@/components/Cafe/CafeCard";

const SearchResults = ({ searchQuery, storedCafes }) => {
  // Pour l'instant, on fait la recherche dans les cafés déjà chargés au lieu de
  // faire une requête au serveur.

  // const { data, isLoading, error } = useApi(`/search?query=${searchQuery}`);
  const normalizedQuery = searchQuery
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();

  const cafes = storedCafes.filter((cafe) => {
    const nameNormalized = cafe.name
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
    return nameNormalized.includes(normalizedQuery);
  });

  if (cafes?.length === 0) {
    return (
      <div className="mt-20 mb-36">
        <EmptyState name="café" />
      </div>
    );
  }

  return (
    <>
      <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
        {cafes.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.slug} />
        ))}
      </div>
    </>
  );
};

export default SearchResults;
