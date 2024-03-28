// import EmptyState from "@/components/EmptyState";
// import { CafeCard } from "@/components/Cafe/CafeCard";
// // import useApi from "@/hooks/useApi";
// // import {ItemCard} from "@/components/Items/ItemCard";

// const SearchResults = ({ searchQuery, storedCafes}) => {
//   // Pour l'instant, on fait la recherche dans les cafés déjà chargés au lieu de
//   // faire une requête au serveur.

//   // const { data, isLoading, error } = useApi(`/search?query=${searchQuery}`);
//   const normalizedQuery = searchQuery
//     .normalize("NFD")
//     .replace(/[\u0300-\u036f]/g, "")
//     .toLowerCase();

//   const cafes = storedCafes.filter((cafe) => {
//     const nameNormalized = cafe.name
//       .normalize("NFD")
//       .replace(/[\u0300-\u036f]/g, "")
//       .toLowerCase();
//     return nameNormalized.includes(normalizedQuery);
//   });

//   if (cafes?.length === 0) {
//     return (
//       <div className="mt-20 mb-36">
//         <EmptyState name="café" />
//       </div>
//     );
//   }
//   console.log(cafes);

//   return (
//     <>
//       <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
//         {cafes.map((cafe) => (
//           <CafeCard cafe={cafe} key={cafe.slug} />
//         ))}
//       </div>
//     </>
//   );
// };


// export default SearchResults;

//Version 2 avec la recherche par item et cafe dans l'application
import useApi from "@/hooks/useApi"; 
import EmptyState from "@/components/EmptyState";
import { CafeCard } from "@/components/Cafe/CafeCard";


const SearchResults = ({ searchQuery }) => {
  const { data: searchResults} = useApi(`/search?query=${searchQuery}`);


  if (!searchResults || searchResults.matching_cafesssss_and_items.length === 0) {
    return <EmptyState name="café" />;
  }
  
 
  const finalResults = searchResults.matching_cafesssss_and_items; //Array des resultats

  return (
    <>
      <div className="relative top-1 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
        {finalResults.map((result) => (
          <CafeCard key={result.slug || result.item_id} cafe={result} />
        ))}
      </div>
    </>
  );
};

export default SearchResults;
