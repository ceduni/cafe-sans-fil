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
import { getCafeCategories, getItemByCategory } from "@/utils/items";
import Breadcrumbs from "@/components/Breadcrumbs";
import { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/24/solid";
import classNames from "classnames";

const Cafe = () => {
  const { id: cafeSlug } = useParams();
  const { data, isLoading, error } = useApi(`/cafes/${cafeSlug}`);
  const [showOpeningHours, setShowOpeningHours] = useState(false);

  const toggleOpeningHours = () => {
    setShowOpeningHours(!showOpeningHours);
  };

  if (error) {
    if (error.status === 404) {
      throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
    }
    return <EmptyState type="error" error={error} />;
  }

  const menuItems = data?.menu_items;
  const categories = getCafeCategories(menuItems);

  return (
    <>
      <Helmet>{data?.name && <title>{data.name} | Café sans-fil</title>}</Helmet>
      <Container className="py-10 pb-12">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item isLoading={isLoading}>{data?.name}</Breadcrumbs.Item>
        </Breadcrumbs>

        <CafeMemberHeader cafe={data} />

        <img
          className="mb-6 rounded-3xl shadow-xl object-cover md:h-[25rem] w-full"
          src={data?.image_url || "https://placehold.co/700x400?text=..."}
          alt={`Photo du café ${data?.name}`}
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = "https://placehold.co/700x400?text=:/";
          }}
        />

        {(isLoading && <div className="animate-pulse h-10 w-1/5 bg-gray-200 rounded-full" />) || (
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{data?.name}</h2>
        )}

        <div className="flex items-center justify-start space-x-2">
          <OpenIndicator
            isOpen={data?.is_open}
            openingHours={data?.opening_hours}
            statusMessage={data?.status_message}
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
          {showOpeningHours && <OpeningHours openingHours={data?.opening_hours} />}
        </div>

        <div className="pb-3 pt-3">
          {(data?.description && (
            <p className="sm:text-lg leading-8 text-gray-600 max-w-3xl">{data?.description}</p>
          )) || (
            <>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5"></div>
              <div className="h-2 bg-gray-200 rounded-full mb-2.5 w-3/4"></div>
            </>
          )}
        </div>

        <div className="flex items-center mb-1">
          <MapPinIcon className="inline-block w-5 h-5 text-gray-500" />
          <span className="ml-1 text-gray-500">{displayCafeLocation(data?.location)}</span>
        </div>

        {!isLoading && <PaymentMethods arrayOfMethods={data?.payment_methods} />}

        {!isLoading && <SocialIcons socialMedia={data?.social_media} />}

        {data?.additional_info?.map(
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
      </Container>

      <Container className="pt-12 border-t border-gray-200">
        <h2 className=" text-4xl text-center font-bold text-gray-900 tracking-wide">Menu</h2>
      </Container>

      {categories.map((category) => (
        <Container key={category} className="py-10">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">{category}</h2>
          <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-4 lg:gap-x-8 items-start">
            {getItemByCategory(menuItems, category).map((product) => (
              <ItemCard key={product.item_id} item={product} cafeSlug={cafeSlug} />
            ))}
          </div>
        </Container>
      ))}

      <Container className="py-12 border-t border-gray-200">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900">Nous contacter</h2>
        <ContactCafe contact={data?.contact} socialMedia={data?.social_media} />
      </Container>
    </>
  );
};

export default Cafe;
