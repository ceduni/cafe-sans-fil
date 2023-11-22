import { useEffect, useState } from "react";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import Container from "@/components/Container";
import { getCafeFromId, getItemFromId } from "@/utils/getFromId";
import EmptyState from "@/components/EmptyState";
import { useAuth } from "@/hooks/useAuth";
import { formatDate } from "@/utils/orders";
import { Tab } from "@headlessui/react";
import classNames from "classnames";
import { LoadingOrderCard, OrderCard } from "@/components/Orders/OrderCard";

function Orders() {
  const { user } = useAuth();

  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [fullOrders, setFullOrders] = useState([]);
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

  // On formate les données des commandes
  useEffect(() => {
    const fullOrders = orders.map(async (order) => {
      // On formate la date
      order.created_at = formatDate(order.created_at);

      // On récupère les données du café
      let cafe = await getCafeFromId(order.cafe_slug);
      if (!cafe) {
        cafe = {
          name: "Café supprimé",
        };
      }

      // On récupère les données des items
      const items = await Promise.all(
        // Pour chaque item de la commande, on récupère les données de l'item
        order.items.map(async (item) => {
          let itemData = await getItemFromId(item.item_slug, order.cafe_slug);
          if (!itemData) {
            itemData = {
              name: "Item supprimé",
              price: item.item_price,
              quantity: item.quantity,
            };
          }
          return {
            ...item,
            itemData: itemData, // On ajoute les données de l'item
          };
        })
      );
      return {
        ...order,
        cafe: cafe,
        items: items,
      };
    });

    Promise.all(fullOrders).then((data) => {
      setFullOrders(data);
    });
  }, [orders]);

  useEffect(() => {
    if (fullOrders.length > 0) {
      setIsLoading(false);
    }
  }, [fullOrders]);

  const isPendingOrder = (status) => {
    return status === "Placée" || status === "Prête";
  };

  const displayedOrders = showOldOrders ? fullOrders.filter((order) => !isPendingOrder(order.status)) : fullOrders;
  console.log(displayedOrders);

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
    <Container className="py-10">
      <div className="flex flex-col items-center">
        <h1 className="text-3xl font-semibold tracking-tight text-gray-900 font-secondary">Mes commandes</h1>

        {!isLoading && orders.length === 0 && <EmptyState name="commande" genre="féminin" />}

        {isLoading && (
          <div className="flex flex-col mt-10 gap-4 w-full max-w-2xl">
            {Array.from({ length: 2 }).map((_, index) => (
              <LoadingOrderCard key={index} />
            ))}
          </div>
        )}

        <div className="w-full max-w-md px-2 py-16 sm:px-0">
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
                  {category.name}
                </Tab>
              ))}
            </Tab.List>
          </Tab.Group>
        </div>

        <div className="flex flex-col mt-10 gap-4 w-full max-w-2xl">
          {displayedOrders.map((order) => (
            <OrderCard order={order} key={order.order_id} />
          ))}
        </div>
      </div>
    </Container>
  );
}

export default Orders;
