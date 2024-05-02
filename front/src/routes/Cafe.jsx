import { useParams } from "react-router-dom";
import ItemCard from "@/components/Items/ItemCard";
import Container from "@/components/Container";
import OpeningHours from "@/components/Cafe/OpeningHours";
import CafeMemberHeader from "@/components/Cafe/CafeMemberHeader";
import useApi from "@/hooks/useApi";
import OpenIndicator from "@/components/Cafe/OpenIndicator";
import EmptyState from "@/components/EmptyState";
import { Helmet } from "react-helmet-async";
import PaymentMethods from "@/components/Cafe/PaymentMethods";
import ContactCafe from "@/components/Cafe/ContactCafe";
import SocialIcons from "@/components/Cafe/SocialIcons";
import { MapPinIcon } from "@heroicons/react/24/solid";
import { displayCafeLocation, shouldDisplayInfo } from "@/utils/cafe";
// import { getCafeCategories, getItemByCategory } from "@/utils/items";
import Breadcrumbs from "@/components/Breadcrumbs";
import { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/solid";
import classNames from "classnames";
import Menu from "./Menu";
import EventBoard from "./Board/eventBoard";
import NewsBoard from "./Board/NewsBoard";
import CafeDescriptionBoard from "./Board/CafeDescriptionBoard";
import { useEffect } from "react";


const Cafe = () => {
  const { id: cafeSlug } = useParams();
  const { data: cafeData, isLoading, error } = useApi(`/cafes/${cafeSlug}`);
  const { data: events, isLoading: eventsLoading, error: eventsError, refetch: refetchEvents } = useApi(`/events/${cafeData ? "?cafe_id=" + cafeData.cafe_id : ''}`, false);
  const { data: announcements, isLoading: announcementsLoading, error: announcementsError, refetch: refetchAnnoucements } = useApi(`/announcements/${cafeData ? "?cafe_id=" + cafeData.cafe_id : ''}`, false);
  const [showOpeningHours, setShowOpeningHours] = useState(false);
  const toggleOpeningHours = () => {
    setShowOpeningHours(!showOpeningHours);
  };
  const [activeCategory, setActiveCategory] = useState(null);

  useEffect(() => {
    if (cafeData && !cafeData.cafe_id &&refetchEvents) {
      refetchEvents();
    }
  }, [cafeData, refetchEvents]); 

  useEffect(() => {
 if(cafeData && !cafeData.cafe_id &&refetchAnnoucements){
  refetchAnnoucements();
 }
  }, [cafeData, refetchAnnoucements]);

  // useEffect(() => {
  //   console.log(cafeData?.staff); // cheker la structure des données reçues
  // }, [cafeData]);

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  if (eventsError) return <EmptyState message="Error loading events" />;

  const menuItems = cafeData?.menu_items;

  if(announcementsError) return <EmptyState message= "Error loading annoucements"/>


  return (
    <>
      <Helmet>{cafeData?.name && <title>{cafeData.name} | Café sans-fil</title>}</Helmet>

        <CafeMemberHeader cafe={cafeData} />


        <div className="relative">
          <img
            className="object-cover md:h-[25rem] w-full"
            src={cafeData?.image_url || "https://placehold.co/700x400?text=..."}
            alt={`Photo du café ${cafeData?.name}`}
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "https://placehold.co/700x400?text=:/";
            }}
          />

          
<div className="absolute top-0 left-1/2 transform -translate-x-1/2 z-10">
        <div className=" top-12 flex items-center justify-start space-x-2 rounded-lg bg-black">
          <OpenIndicator
            isOpen={cafeData?.is_open}
            openingHours={cafeData?.opening_hours}
            statusMessage={cafeData?.status_message}
          />
          <button onClick={toggleOpeningHours}>
            {showOpeningHours ? <ChevronUpIcon className="h-6 w-6" /> : <ChevronDownIcon className="h-6 w-6" />}
          </button>
        </div>

        <div
          className={classNames("overflow-hidden transition-all duration-200", {
            "max-h-0": !showOpeningHours,
            "max-h-96": showOpeningHours,
          })}>
          {showOpeningHours && <OpeningHours openingHours={cafeData?.opening_hours} />}
        </div>
      </div>
<div className="absolute bottom-0 left-0 right-0 p-0 flex  items-center">
    {/* Title container with background */}
    <div className="bg-white px-4 py-2 rounded-r"> {/* Adjust padding and rounded corners as needed */}
      {(isLoading && <div className="animate-pulse h-10 w-1/5 bg-gray-200 rounded-full" />) || (
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          {cafeData?.name}
        </h2>
      )}
    </div>
    
    {/* Social icons container with background */}
    <div className="flex">
    {!isLoading && <SocialIcons socialMedia={cafeData?.social_media} />}
  </div>
</div>
        </div>


        {!isLoading && <PaymentMethods arrayOfMethods={cafeData?.payment_methods} />}


        {cafeData?.additional_info?.map(
          (info, index) =>
            shouldDisplayInfo(info) && (
              <div
                className="bg-sky-50 border border-l-4 border-l-sky-300 p-6 pl-8 mt-4 rounded-2xl"
                role="alert"
                key={index}>
                <h3 className="mb-1 text-lg font-semibold text-gray-900">{info.type}</h3>
                <p className="text-sm">{info.value}</p>
              </div>
            )
        )}
      
      
      <div className="flex flex-wrap md:flex-nowrap">
        {/* Colonne du menu */}
        <div className="w-full md:w-3/5">
          <Menu items={menuItems} />
        </div>

        {/* Colonne de droite pour la boîte de description et les annonces */}
        <div className="w-full md:w-2/5 mt-4 md:mt-0 md:ml-4">
        {cafeData && <CafeDescriptionBoard cafe={cafeData} />}
        
        <NewsBoard cafe={cafeData} news={announcements || []} />
      </div>
      </div>
      
      <EventBoard cafe={cafeData} events={events || []} />

      <Container className="py-12 border-t border-gray-200">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Nous contacter</h2>
        <ContactCafe contact={cafeData?.contact} socialMedia={cafeData?.social_media} />
      </Container>
    </>
  );
};

export default Cafe;
