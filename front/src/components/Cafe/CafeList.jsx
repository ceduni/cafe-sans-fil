import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import Filters from "@/components/Cafe/Filters";
import { useEffect, useState } from "react";
import { isCafeActuallyOpen } from "@/utils/cafe";

const CafeList = ({ setStoredCafes, storedCafes }) => {
  const [filters, setFilters] = useState({
    openOnly: false,
    pavillon: "Tous les pavillons",
  });

  const [data, isLoading, error] = useApi("/cafes");

  useEffect(() => {
    if (data) {
      setStoredCafes(data);
    }
  }, [data, setStoredCafes]);

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  const filteredData = storedCafes.filter(
    (cafe) =>
      (filters.openOnly ? isCafeActuallyOpen(cafe.is_open, cafe.opening_hours) : true) &&
      (filters.pavillon === "Tous les pavillons" || cafe.location.pavillon === filters.pavillon)
  );

  if (isLoading && storedCafes.length === 0) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6 animate-pulse duration-100">
        {Array.from({ length: 8 }).map((_, i) => (
          <CafeCardLoading key={i} />
        ))}
      </div>
    );
  }

  return (
    <>
      <Filters filters={filters} setFilters={setFilters} cafes={storedCafes} />

      {filteredData?.length === 0 && <EmptyState name="café" />}

      <div className="grid animate-fade-in grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
        {filteredData.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.slug} />
        ))}
      </div>
    </>
  );
};

export default CafeList;
