import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import Filters from "@/components/Cafe/Filters";
import { useEffect, useState } from "react";
import { PAYMENT_METHODS, isCafeActuallyOpen } from "@/utils/cafe";
import getCurrentUser from "@/utils/users";
import { useAuth } from "@/hooks/useAuth";

const CafeList = ({ setStoredCafes, storedCafes }) => {
  const [filters, setFilters] = useState({
    openOnly: false,
    pavillon: "Tous les pavillons",
    takesCash: false,
    takesCreditCard: false,
    takesDebitCard: false,
    recommendations: false,
  });

  const { data, isLoading, error } = useApi("/cafes");
  const { isLoggedIn } = useAuth();

  const checkUserStatus = async () => {
    if (isLoggedIn) {
      const currentUser = await getCurrentUser();
      if (currentUser.user_id) {
        return currentUser.user_id;
      }
      return "";
    }
  };

  const { recommendationsData, isloading, errors } = useApi(`/recommendations/cafe/${checkUserStatus()}`);
  const [recommendations, setRecommendations] = useState(["cafekine"]);

  useEffect(() => {
    if (data) {
      setStoredCafes(data);
    }

    if (recommendationsData) {
      setRecommendations(recommendationsData);
    }

  }, [data, setStoredCafes]);
  

  if (error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
  }

  const filteredData = storedCafes.filter(
    (cafe) =>
      (filters.openOnly ? isCafeActuallyOpen(cafe.is_open, cafe.opening_hours) : true) &&
      (filters.pavillon === "Tous les pavillons" || cafe.location.pavillon === filters.pavillon) &&
      (filters.takesCash ? cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.CASH) : true) &&
      (filters.takesCreditCard
        ? cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.CREDIT_CARD)
        : true) &&
      (filters.takesDebitCard
        ? cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.DEBIT_CARD)
        : true) &&
      (filters.recommendations ? recommendations.includes(cafe.slug) : true)
  );

  if (isLoading && storedCafes.length === 0) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100">
        {Array.from({ length: 20 }).map((_, i) => (
          <CafeCardLoading key={i} />
        ))}
      </div>
    );
  }

  return (
    <div className="relative bottom-4 xl:bottom-2">
      <Filters filters={filters} setFilters={setFilters} cafes={storedCafes} />

      {filteredData?.length === 0 && <div className="mt-20 mb-36"><EmptyState name="café" /></div>}

      <div className="grid animate-fade-in grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
        {filteredData.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.slug} />
        ))}
      </div>
    </div>
  );
};

export default CafeList;
