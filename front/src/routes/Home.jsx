import Container from "@/components/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "@/components/Search/SearchBar";
import { useEffect, useState } from "react";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";
import { useAuth } from "@/hooks/useAuth";
import useApi from "@/hooks/useApi";
import getCurrentUser from "@/utils/users";
import Filters from "@/components/Cafe/Filters";
import RecommendedCafeList from "@/components/Cafe/RecommendedCafeList";


const Home = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const isSearching = searchQuery.length > 0;
  const [storedCafes, setStoredCafes] = useState([]);
  const { isLoggedIn } = useAuth();
  const [recommendedCafes, setRecommendedCafes] = useState([]);
  const [shouldRecommend, setShouldRecommend] = useState(true);
  const { data, isLoading, error } = useApi("/cafes");
  //const currentUserRecommendations = useApi(`/recommendations/cafe/${currentUser.user_id}`);
  const currentUserRecommendations = ["cafekine", "la-planck", "lintermed", "pill-pub"];
  const [currentUserDiets, setCurrentUserDiets] = useState([]);



  const [filters, setFilters] = useState({
    openOnly: false,
    pavillon: "Tous les pavillons",
    takesCash: false,
    takesCreditCard: false,
    takesDebitCard: false,
    cafeSellingDietProductOnly: false,
  });


  const getRecommendedCafes = async () => {
    if (isLoggedIn && storedCafes) {
      const filteredCafes = storedCafes.filter((cafe) => currentUserRecommendations.includes(cafe.slug));
      // console.log(filteredCafes);
      setRecommendedCafes(filteredCafes);
    }
  };

  useEffect(() => {
    getRecommendedCafes();
  }, [storedCafes]);


  useEffect(() => {
    if (filters.cafeSellingDietProductOnly || filters.takesCash || 
      filters.takesCreditCard || filters.takesDebitCard || filters.openOnly || filters.pavillon !== "Tous les pavillons") {
      setShouldRecommend(false);
    } else {
      setShouldRecommend(true);
    }
  }, [filters]);
  

  useEffect(() => {
    const currUserDiets = async () => {
      const currentUser = await getCurrentUser();
      setCurrentUserDiets(currentUser.diet_profile?.diets);
    }

    if (isLoggedIn) {
      currUserDiets();
    }
  }, []);

  return (
    <>
      <Helmet>
        <title>Accueil | Café sans-fil</title>
      </Helmet>
      <Container className="pt-10 pb-[3.25rem] sm:py-14 space-y-6">
        <div className="flex gap-2">
          <h1 className="text-3xl sm:text-4xl text-opacity-90 font-secondary text-zinc-800 leading-7">
            Cafés étudiants de l'UdeM
          </h1>
          {/* <a href="https://www.umontreal.ca/" target="_blank" rel="noopener noreferrer" className="my-auto sm:my-0">
            <img src="/udem_logo.png" alt="UdeM Logo" className="h-9 object-contain" />
          </a> */}
        </div>
        <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      </Container>

      <Filters filters={filters} setFilters={setFilters} cafes={storedCafes} isLoggedIn={isLoggedIn} />
      
      { isLoggedIn && !isSearching && shouldRecommend && 
      <div>
        <Container>
          <h2 className="text-2xl sm:text-3xl text-zinc-800 font-secondary text-opacity-90 leading-7">Recommandations</h2>
          <RecommendedCafeList 
            recommendedCafes={recommendedCafes} 
            isLoading={isLoading} 
          />
        </Container>

      </div>}
      <main>
        <Container>
          <h2 className="text-2xl sm:text-3xl text-zinc-800 font-secondary text-opacity-90 leading-7">Tous les cafés</h2>
          {(!isSearching && 
            <CafeList 
              data={data} 
              isLoading={isLoading} 
              error={error} 
              setStoredCafes={setStoredCafes} 
              storedCafes={storedCafes} 
              shouldRecommend={false} 
              currentUserDiets={currentUserDiets} 
              filters={filters} 
            />) || (
            <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
