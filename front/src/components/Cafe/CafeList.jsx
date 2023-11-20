import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import Filters from "@/components/Cafe/Filters";
import { useEffect, useState } from "react";
import { isCafeActuallyOpen } from "@/utils/cafe";

const CafeList = ({ setStoredCafes }) => {
  const [filters, setFilters] = useState({
    openOnly: false,
    pavillon: "Tous les pavillons",
  });

  const [data, isLoading, error] = useApi("/cafes");

  useEffect(() => {
    setStoredCafes(data);
  }, [data]);

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  const filteredData =
    (data &&
      data.filter(
        (cafe) =>
          (filters.openOnly ? isCafeActuallyOpen(cafe.is_open, cafe.opening_hours) : true) &&
          (filters.pavillon === "Tous les pavillons" || cafe.location.pavillon === filters.pavillon)
      )) ||
    [];

  return (
    <>
      <Filters filters={filters} setFilters={setFilters} cafes={data} />

      {filteredData?.length === 0 && !isLoading && <EmptyState name="café" />}

      {isLoading && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6 animate-pulse duration-100">
          {Array.from({ length: 8 }).map((_, i) => (
            <CafeCardLoading key={i} />
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
        {filteredData?.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.slug} />
        ))}
      </div>
    </>
  );
};

export default CafeList;
