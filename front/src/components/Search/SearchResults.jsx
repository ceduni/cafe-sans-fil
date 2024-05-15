//recherche par item et tag dans l'application
import useApi from "@/hooks/useApi"; 
import EmptyState from "@/components/EmptyState";
import { CafeCard } from "@/components/Cafe/CafeCard";


const SearchResults = ({ searchQuery }) => {
  const { data: searchResults} = useApi(`/search?query=${searchQuery}`);


  if (!searchResults || searchResults.matching_cafes_and_their_items.length === 0) {
    return <EmptyState name="café" />;
  }
  
 
  const finalResults = searchResults.matching_cafes_and_their_items; //Array des resultats

  return (
    <>
      <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
        {finalResults.map((result) => (
          <CafeCard key={result.slug || result.item_id} cafe={result} searchQuery={searchQuery} />
        ))}
      </div>
    </>
  );
};

export default SearchResults;
