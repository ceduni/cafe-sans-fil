import EmptyState from "@/components/EmptyState";
import { CafeCard } from "@/components/Cafe/CafeCard";

const SearchResults = ({ searchQuery, storedCafes }) => {
  // Pour l'instant, on fait la recherche dans les cafés déjà chargés au lieu de
  // faire une requête au serveur.

  // const [data, isLoading, error] = useApi(`/search?query=${searchQuery}`);

  const cafes = storedCafes.filter(
    (cafe) =>
      cafe.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cafe.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (cafes?.length === 0) {
    return <EmptyState name="café" />;
  }

  return (
    <>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
        {cafes.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.cafe_id} />
        ))}
      </div>
    </>
  );
};

export default SearchResults;
