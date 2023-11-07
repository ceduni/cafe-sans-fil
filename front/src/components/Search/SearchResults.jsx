import useApi from "@/hooks/useApi";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";

const SearchResults = ({ searchQuery }) => {
  const [data, isLoading, error] = useApi(`/search?query=${searchQuery}`);
  const cafes = data?.matching_cafes || [];

  if (error) {
    return <EmptyState type="error" error={error} />;
  }

  if (cafes?.length === 0) {
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
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 py-6">
        {cafes.map((cafe) => (
          <CafeCard cafe={cafe} key={cafe.cafe_id} />
        ))}
      </div>
    </>
  );
};

export default SearchResults;
