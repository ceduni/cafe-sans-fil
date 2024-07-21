import Container from "@/components/Container";
import { Helmet } from "react-helmet-async";
import SearchBar from "@/components/Search/SearchBar";
import { useEffect, useState } from "react";
import CafeList from "@/components/Cafe/CafeList";
import SearchResults from "@/components/Search/SearchResults";
import { useAuth } from "@/hooks/useAuth";

const Home = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const isSearching = searchQuery.length > 0;
  const [storedCafes, setStoredCafes] = useState([]);

  const { isLoggedIn } = useAuth();
  const [recommendedCafes, setRecommendedCafes] = useState([]);

  const getRecommendedCafes = async () => {
    if (isLoggedIn && storedCafes) {
      // const currentUser = await getCurrentUser();
      // const currentUserRecommendations = useApi(`/recommendations/cafe/${currentUser.user_id}`);
      const currentUserRecommendations = ["cafekine", "la-planck", "lintermed", "pill-pub"];
      const filteredCafes = storedCafes.filter((cafe) => currentUserRecommendations.includes(cafe.slug));
      // console.log(filteredCafes);
      setRecommendedCafes(filteredCafes);
    }
  };

  useEffect(() => {
    getRecommendedCafes();
  }, [storedCafes]);

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
      { isLoggedIn && <div>
        <Container>
          <h2 className="text-2xl sm:text-3xl text-zinc-800 font-secondary text-opacity-90 leading-7">Recommandations</h2>
          {(!isSearching && <CafeList setStoredCafes={setRecommendedCafes} storedCafes={recommendedCafes} shouldRecommend={true} />) || (
            <SearchResults searchQuery={searchQuery} storedCafes={recommendedCafes} />
          )}
        </Container>
      </div>}
      <main>
        <Container>
          <h2 className="text-2xl sm:text-3xl text-zinc-800 font-secondary text-opacity-90 leading-7">Tous les cafés</h2>
          {(!isSearching && <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} shouldRecommend={false} />) || (
            <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
          )}
        </Container>
      </main>
    </>
  );
};

export default Home;
