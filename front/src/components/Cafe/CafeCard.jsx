import { Link } from "react-router-dom";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import Card from "@/components/Card";
import { displayCafeLocation, shouldDisplayInfo } from "@/utils/cafe";
import { ChevronRightIcon } from "@heroicons/react/24/solid";

const CafeCard = ({ cafe }) => {
  return (
    <Link
      to={`/cafes/${cafe.slug}`}
      className="contents select-none"
      onKeyDown={(e) => e.key === "Enter" && e.target.click()}>
      <Card>
        <Card.Image src={cafe.image_url} alt={cafe.name} />
        <Card.Header>
          <Card.Header.Title>{cafe.name}</Card.Header.Title>
          <Card.Header.Subtitle>{displayCafeLocation(cafe.location)}</Card.Header.Subtitle>
          <OpenIndicator
            isOpen={cafe.is_open}
            openingHours={cafe.opening_hours}
            statusMessage={cafe.status_message}
            size="xs"
          />
        </Card.Header>
        <Card.Body>{cafe.description}</Card.Body>
        {cafe.additional_info && cafe.additional_info[0]?.value && shouldDisplayInfo(cafe.additional_info[0]) && (
          <Card.Footer>
            <div
              className="px-4 bg-sky-200 rounded-full animate-text flex lg:inline-flex items-center justify-between gap-2 w-fit max-w-full"
              role="alert">
              <span className="py-2 leading-none font-semibold text-xs text-gray-700" style={{ textWrap: "balance" }}>
                {cafe.additional_info[0].value}
              </span>
              <ChevronRightIcon className="w-4 h-4 flex-shrink-0 opacity-75" />
            </div>
          </Card.Footer>
        )}
      </Card>
    </Link>
  );
};

const CafeCardLoading = () => {
  return (
    <Card>
      <Card.Header>
        <Card.Header.Title as="div">
          <div className="h-3 bg-gray-200 rounded-full w-36 mb-4"></div>
        </Card.Header.Title>
        <Card.Header.Subtitle as="div">
          <div className="h-2.5 bg-gray-200 rounded-full w-48 mb-4"></div>
        </Card.Header.Subtitle>
      </Card.Header>
      <Card.Body>
        <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
        <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
        <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
        <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
        <div className="h-2 bg-gray-200 rounded-full"></div>
      </Card.Body>
    </Card>
  );
};

export { CafeCard, CafeCardLoading };
