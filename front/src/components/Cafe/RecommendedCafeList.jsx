import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import EmptyState from "@/components/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { useEffect, useState } from "react";
import { UserCafeRecommendationAPI } from "@/utils/api";

function renderError(error) {
  return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
}

function renderEmpty() {
  return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100">
          {Array.from({ length: 4 }).map((_, i) => (
              <CafeCardLoading key={i} />
          ))}
      </div>
  );
}

function getRecommendedCafes(storedCafes, recommendedCafesSlug) {
  if (recommendedCafesSlug.length === 0) {
    return [];
  }
  const result = storedCafes.filter((cafe) => recommendedCafesSlug.includes(cafe.slug));
  return result;
}

const RecommendedCafeList = ({ storedCafes, filters }) => {

  const [recommendedCafes, setRecommendedCafes] = useState([]);
  const { isLoggedIn } = useAuth()
  //const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isLoggedIn) {
      UserCafeRecommendationAPI.get(isLoggedIn.user_id)
      .then((data) => {
        setRecommendedCafes(getRecommendedCafes(storedCafes, data));
      })
      .catch((error) => {
        setError(error)
      });
    }
  }, [storedCafes]);


  if (error) {
    console.trace(error);
    return renderError(error);
  }

  // if (isLoading && recommendedCafes.length === 0) {
  //   return renderEmpty();
  // }

  const bestCafes = recommendedCafes.length > 4 ? recommendedCafes.slice(0, 4) : recommendedCafes;
  
  return (
      !filters.openOnly && !filters.takesCash && !filters.takesCreditCard && !filters.takesDebitCard &&
      <>
        { isLoggedIn && <h1 className="text-3xl font-bold text-gray-900">Recommendations</h1> }
        <div className="grid animate-fade-in grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
            { bestCafes.length > 0 && isLoggedIn ? (
              bestCafes.map((cafe) => (
              <CafeCard cafe={cafe} key={cafe.slug} />))
              )
              : null
            }
        </div>
      </>
  )
}

export default RecommendedCafeList;