import { Link } from "react-router-dom";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import Card from "@/components/Card";
import { displayCafeLocation, shouldDisplayInfo } from "@/utils/cafe";
import { ChevronRightIcon } from "@heroicons/react/24/solid";
import { useEffect, useState } from "react";
import getCurrentUser from "@/utils/users";
import { useAuth } from "@/hooks/useAuth";

const CafeCard = ({ cafe, recommendations }) => {
  const [isRecommended, setIsRecommended] = useState(false);
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    const checkIsRecommended = async () => {
      //const currentUser = await getCurrentUser();
      //const { recommendationsData, isloading, errors } = useApi(`/recommendations/cafe/${currentUser.username}`);
      //setRecommendations(recommendationsData);
      if (recommendations ? recommendations.includes(cafe.slug) : false) {
        setIsRecommended(true)
      }
    };

    checkIsRecommended()
  
  }, [])

  return (
    <Link
      to={`/cafes/${cafe.slug}`}
      className="contents select-none"
      onKeyDown={(e) => e.key === "Enter" && e.target.click()}>
      <Card>
        <Card.Image src={cafe.image_url} alt={cafe.name} />
        {/* <div className="relative w-min p-4 rounded-lg">
          {
            isLoggedIn && isRecommended && (
              <div className="absolute top-0 left-0 text-green-500 bg-white opacity-90 px-3 py-1 rounded-md font-bold">
                Recommendé
              </div>
            )
          }
        </div> */}
        <Card.Header>
          <Card.Header.Title>{cafe.name}</Card.Header.Title>
          <Card.Header.Subtitle>{displayCafeLocation(cafe.location)}</Card.Header.Subtitle>
          <OpenIndicator
            isOpen={cafe.is_open}
            openingHours={cafe.opening_hours}
            statusMessage={cafe.status_message}
            size="xs"
          />
          {cafe.additional_info && cafe.additional_info[0]?.value && shouldDisplayInfo(cafe.additional_info[0]) && (
            <div
              className="mt-4 px-4 animate-text bg-sky-200 rounded-full flex items-center justify-center gap-2 w-fit"
              role="alert">
              <span className="py-2 leading-none font-semibold text-xs text-gray-700">
                {cafe.additional_info[0].value}
              </span>
              <ChevronRightIcon className="w-4 h-4 flex-shrink-0 opacity-75" />
            </div>
          )}
        </Card.Header>
      </Card>
    </Link>
  );
};

const CafeCardLoading = () => {
  return (
    <Card>
      <Card.Header>
        <Card.Header.Title as="div">
          <div className="h-14 sm:h-16 bg-white rounded-full mb-2.5"></div>
        </Card.Header.Title>
        <Card.Header.Subtitle as="div">

        </Card.Header.Subtitle>
      </Card.Header>
      <Card.Body>
        <div className="h-2.5 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
        <div className="h-2.5 bg-gray-200 rounded-full mb-2.5"></div>
        <div className="h-2.5 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
      </Card.Body>
    </Card>
  );
};

export { CafeCard, CafeCardLoading };
