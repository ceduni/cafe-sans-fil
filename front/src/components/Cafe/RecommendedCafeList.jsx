import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import EmptyState from "@/components/EmptyState";

const RecommendedCafeList = ({ recommendedCafes, isLoading, error }) => {
    const bestCafes = recommendedCafes.length > 4 ? recommendedCafes.slice(0, 4) : recommendedCafes;

    if (error) {
      return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
    }
    
    if (isLoading && recommendedCafes.length === 0) {
        return (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100">
            {Array.from({ length: 20 }).map((_, i) => (
              <CafeCardLoading key={i} />
            ))}
          </div>
        );
    }

    return (
        <div className="grid animate-fade-in grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
            {bestCafes.map((cafe) => (
            <CafeCard cafe={cafe} key={cafe.slug} />
            ))}
        </div>
    )
}

export default RecommendedCafeList;