import { useEffect, useState } from "react";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import Container from "@/components/Container";
import EmptyState from "@/components/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { formatDate, isOldOrder } from "@/utils/orders";
import { Tab } from "@headlessui/react";
import classNames from "classnames";
import { LoadingOrderCard, OrderCard } from "@/components/Orders/OrderCard";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";

function Orders() {
  const { user } = useAuth();

  const [orders, setOrders] = useState([]);
  const [areOrdersLoading, setIsLoading] = useState(true);
  const [showOldOrders, setShowOldOrders] = useState(false);

  // On récupère les commandes de l'utilisateur
  useEffect(() => {
    const fetchOrders = async () => {
      const response = await authenticatedRequest(`/users/${user.username}/orders`);
      setOrders(response.data);
      if (response.data.length === 0) {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchOrders();
    }
  }, [user]);

  // On récupère les cafés pour afficher les images et les noms
  const [data, isLoading] = useApi(`/cafes`);
  const cafes = data || [];
  const getCafeFromSlug = (slug) => {
    if (isLoading) return {};
    return cafes.find((cafe) => cafe.slug === slug);
  };

  // On formate les données des commandes
  const formatedOrders = orders.map((order) => ({ ...order, created_at: formatDate(order.created_at) }));
  useEffect(() => {
    if (formatedOrders.length > 0) {
      setIsLoading(false);
    }
  }, [formatedOrders]);

  const oldOrdersCount = formatedOrders.filter((order) => isOldOrder(order.status)).length;
  const pendingOrdersCount = formatedOrders.length - oldOrdersCount;

  const displayedOrders = showOldOrders
    ? formatedOrders.filter((order) => isOldOrder(order.status))
    : formatedOrders.filter((order) => !isOldOrder(order.status));
  displayedOrders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // On trie les commandes par date

  const tabCategories = [
    {
      name: "En cours",
      onClick: () => setShowOldOrders(false),
    },
    {
      name: "Terminées",
      onClick: () => setShowOldOrders(true),
    },
  ];

  return (
    <>
      <Helmet>
        <title>Mes commandes | Café sans-fil</title>
      </Helmet>
      <Container className="py-12 md:py-14">
        <div className="flex flex-col items-center">
          <h1 className="text-3xl tracking-tight text-opacity-80 font-secondary text-zinc-800">Mes commandes</h1>

          {areOrdersLoading && (
            <div className="flex flex-col mt-10 gap-4 w-full max-w-2xl">
              {Array.from({ length: 2 }).map((_, index) => (
                <LoadingOrderCard key={index} />
              ))}
            </div>
          )}

          <div className="w-full max-w-md px-2 py-10 sm:px-0">
            <Tab.Group>
              <Tab.List className="flex space-x-1 rounded-xl bg-emerald-900/20 p-1">
                {tabCategories.map((category) => (
                  <Tab
                    key={category.name}
                    className={({ selected }) =>
                      classNames(
                        selected ? "bg-white text-emerald-700 shadow" : "text-gray-600 hover:bg-white/[0.12]",
                        "w-full rounded-lg py-2.5 text-sm font-medium leading-5",
                        "ring-white/60 ring-offset-2 ring-offset-gray-400 focus:outline-none focus:ring-2"
                      )
                    }
                    onClick={category.onClick}>
                    {category.name} ({category.name === "En cours" ? pendingOrdersCount : oldOrdersCount})
                  </Tab>
                ))}
              </Tab.List>
            </Tab.Group>
          </div>

          {!areOrdersLoading && orders.length === 0 && <EmptyState name="commande" genre="féminin" />}

          <div className="flex flex-col mt-4 gap-4 w-full max-w-2xl">
            {displayedOrders.map((order) => (
              <OrderCard order={order} cafe={getCafeFromSlug(order.cafe_slug)} key={order.order_id} />
            ))}
          </div>
        </div>
      </Container>
    </>
  );
}

export default Orders;
