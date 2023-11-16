import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import Filters from "@/components/Cafe/Filters";
import { useEffect, useState } from "react";

const CafeList = ({ setStoredCafes }) => {
  const [filters, setFilters] = useState({
    openOnly: false,
    pavillon: "Tous les pavillons",
  });

  const [data, isLoading, error] = useApi("/cafes" + (filters.openOnly ? "?is_open=true" : ""));

  useEffect(() => {
    setStoredCafes(data);
  }, [data]);

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  const filteredData =
    filters.pavillon === "Tous les pavillons"
      ? data
      : data.filter((cafe) => cafe.location.pavillon === filters.pavillon);

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
          <CafeCard cafe={cafe} key={cafe.cafe_id} />
        ))}
      </div>
    </>
  );
};

export default CafeList;
