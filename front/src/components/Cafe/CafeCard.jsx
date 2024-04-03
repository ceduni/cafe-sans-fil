import { Link } from "react-router-dom";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import Card from "@/components/Card";
import { displayCafeLocation, shouldDisplayInfo } from "@/utils/cafe";
import { ChevronRightIcon } from "@heroicons/react/24/solid";

const CafeCard = ({ cafe ,searchQuery}) => {

  // Trouvez l'item de menu  ou tag recherché
  const searchedMenuItem = searchQuery
    ? cafe.menu_items.filter((item) =>
        item.name.toLowerCase().includes(searchQuery.toLowerCase()), //pour les items
      )
    : [];

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


        {/* {searchedMenuItem && ( // affichage du preview si l'item est trouvé
                  <div
                    className="mt-4 px-4 bg-blue-100 rounded-full flex items-center justify-center gap-2 w-fit"
                    role="alert"
                  >
                    <span className="py-2 leading-none font-semibold text-xs text-blue-800">
                      Menu: {searchedMenuItem.name} - ${searchedMenuItem.price}
                    </span>
                  </div>
                )} */}


{/* version avec le tout en fond bleu */}
{/* {searchedMenuItem.length > 0 && (
            searchedMenuItem.map((item) => (
              <div key={item.item_id} className="mt-4 px-4 bg-blue-100 rounded-full flex items-center justify-center gap-2 w-fit" role="alert">
                <span className="py-2 leading-none font-semibold text-xs text-blue-800">
                  Menu: {item.name} - ${item.price}
                </span>
              </div>
            ))
          )} */}

{/* version avec seulement Menu en fond bleu */}
{searchedMenuItem.length > 0 && (
            <>
              <div className="mt-4 px-4 bg-blue-100 rounded-full flex items-center justify-center gap-2 w-fit" role="alert">
                <span className="py-2 leading-none font-semibold text-xs text-blue-800">Menu:</span>
              </div>
              <div className="flex flex-col items-center justify-center gap-2 w-fit">
                {searchedMenuItem.map((item) => (
                  <span key={item.item_id} className="leading-none font-semibold text-xs text-blue-800">
                    {item.name} - ${item.price}
                  </span>
                ))}
              </div>
            </>
          )}
          
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
