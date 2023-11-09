import { useEffect, useState } from "react";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import Container from "@/components/Container";
import { getCafeFromId, getItemFromId } from "@/helpers/getFromId";
import EmptyState from "@/components/EmptyState";
import { useAuth } from "@/hooks/useAuth";

function Orders() {
  const { user } = useAuth();

  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [fullOrders, setFullOrders] = useState([]);

  // On récupère les commandes de l'utilisateur
  useEffect(() => {
    const fetchOrders = async () => {
      const response = await authenticatedRequest(`/users/${user.user_id}/orders`);
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
      order.order_timestamp = new Intl.DateTimeFormat("fr-FR", {
        dateStyle: "medium",
        timeStyle: "short",
      }).format(new Date(order.order_timestamp));

      // On récupère les données du café
      const cafe = await getCafeFromId(order.cafe_id);

      // On récupère les données des items
      const items = await Promise.all(
        // Pour chaque item de la commande, on récupère les données de l'item
        order.items.map(async (item) => {
          const itemData = await getItemFromId(item.item_id, order.cafe_id);
          return {
            ...item,
            itemData: itemData,
          };
        })
      );
      setIsLoading(false);
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

  return (
    <Container className="py-10">
      <div className="flex flex-col items-center">
        <h1 className="text-3xl font-semibold tracking-tight text-gray-900 font-secondary">Mes commandes</h1>

        {!isLoading && orders.length === 0 && <EmptyState name="commande" genre="féminin" />}

        {isLoading && (
          <div className="flex flex-col mt-10 gap-4 w-full max-w-2xl">
            {Array.from({ length: 2 }).map((_, index) => (
              <div key={index} className="flex flex-col p-6 border border-gray-200 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-12 h-12 mr-4 rounded-full bg-gray-200 animate-pulse"></div>
                    <div>
                      <div className="w-32 h-4 mb-2 rounded-full bg-gray-200 animate-pulse"></div>
                      <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
                    </div>
                  </div>
                  <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
                </div>

                <hr className="my-6 border-gray-200" />

                <div>
                  {Array.from({ length: 3 }).map((_, index) => (
                    <div key={index} className="flex items-center justify-between mb-6 last:mb-0">
                      <div className="flex items-center">
                        <div className="w-8 h-8 mr-4 rounded-lg bg-gray-200 animate-pulse"></div>
                        <div>
                          <div className="w-32 h-4 mb-2 rounded-full bg-gray-200 animate-pulse"></div>
                          <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
                        </div>
                      </div>
                      <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="flex flex-col mt-10 gap-4 w-full max-w-2xl">
          {fullOrders.map((order) => (
            <div key={order.order_id} className="flex flex-col p-6 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <img
                    className="w-12 h-12 mr-4 rounded-full"
                    src="https://placehold.co/300x300?text=Cafe"
                    alt={order.cafe.name}
                  />
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">{order.cafe.name}</h2>
                    <p className="text-sm text-gray-500">{order.order_timestamp}</p>
                  </div>
                </div>
                <p className="text-lg font-semibold text-gray-900">{order.total_price} $</p>
              </div>

              <hr className="my-6 border-gray-200" />

              <div>
                {order.items.map((item, index) => (
                  <div key={index} className="flex items-center justify-between mb-6 last:mb-0">
                    <div className="flex items-center">
                      <img
                        className="w-8 h-8 mr-4 rounded-lg"
                        src="https://placehold.co/300x300?text=Item"
                        alt={item.itemData.name}
                      />
                      <div>
                        <h3 className="text-base font-semibold text-gray-900">{item.itemData.name}</h3>
                        <p className="text-sm text-gray-500">
                          Quantité: {item.quantity} x {item.itemData.price} $
                        </p>
                      </div>
                    </div>
                    <p className="text-base font-semibold text-gray-900">{item.quantity * item.itemData.price} $</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </Container>
  );
}

export default Orders;
