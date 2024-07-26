import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";

const RecommendedCafeList = ({ recommendedCafes, isLoading }) => {

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
            {recommendedCafes.map((cafe) => (
            <CafeCard cafe={cafe} key={cafe.slug} />
            ))}
        </div>
    )

}

export default RecommendedCafeList;