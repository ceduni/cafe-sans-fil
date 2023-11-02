import useApi from "../hooks/useApi";
import EmptyState from "./ui/EmptyState";
import { CafeCard, CafeCardLoading } from "./ui/CafeCard";
import Filters from "./ui/Filters";
import { useState, useEffect } from "react";

const CafeList = () => {
  const { data: cafeList, isLoading, error } = useApi("/cafes");

  const [filters, setFilters] = useState({
    openOnly: false,
    payment: [],
  });

  useEffect(() => {
    console.log(filters);
  }),
    [filters];

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  if (cafeList?.length === 0) {
    return <EmptyState name="café" />;
  }

  if (isLoading) {
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
      <Filters filters={filters} setFilters={setFilters} />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
        {cafeList.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.cafe_id} />
        ))}
      </div>
    </>
  );
};

export default CafeList;
