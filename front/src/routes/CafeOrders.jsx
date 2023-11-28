import Container from "@/components/Container";
import CafeOrderCard from "@/components/Orders/CafeOrderCard";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { ORDER_STATUS, isPendingOrder } from "@/utils/orders";
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import toast from "react-hot-toast";
import ErrorState from "@/components/ErrorState";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";

const CafeOrders = () => {
  const { id: cafeSlug } = useParams();

  const [orders, setOrders] = useState([]);
  const [areOrdersLoading, setAreOrdersLoading] = useState(true);
  const [isUnothorized, setIsUnauthorized] = useState(false);

  const [data, isLoading] = useApi(`/cafes/${cafeSlug}`);
  const cafeName = isLoading ? "Chargement..." : data.name;

  // On récupère les commandes du café
  useEffect(() => {
    const fetchOrders = async () => {
      authenticatedRequest
        .get(`/cafes/${cafeSlug}/orders`)
        .then((response) => {
          const orders = response.data.filter((order) => isPendingOrder(order.status));
          setOrders(orders);
          if (orders.length === 0) {
            setAreOrdersLoading(false);
          }
        })
        .catch((error) => {
          if (error.response.status === 403) {
            setIsUnauthorized(true);
            return;
          }
          toast.error("Erreur lors de la récupération des commandes");
        });
    };

    fetchOrders();
  }, []);

  useEffect(() => {
    if (orders.length > 0) {
      setAreOrdersLoading(false);
    }
  }, [orders]);

  const updateOrderStatus = async (orderId, newStatus) => {
    const payload = {
      status: newStatus,
    };
    const toastId = toast.loading("Mise à jour de la commande...");
    const response = await authenticatedRequest.put(`/orders/${orderId}`, payload);
    if (response.status !== 200) {
      toast.error("Erreur lors de la mise à jour de la commande");
      return;
    }
    (newStatus === ORDER_STATUS.READY && toast.success("Commande complétée!")) || toast.success("Commande annulée!");
    setOrders(orders.filter((order) => order.order_id !== orderId)); // On retire la commande de la liste
    toast.dismiss(toastId);
  };
  const setOrderReady = (orderId) => {
    updateOrderStatus(orderId, ORDER_STATUS.READY);
  };
  const setOrderCanceled = (orderId) => {
    updateOrderStatus(orderId, ORDER_STATUS.CANCELED);
  };

  if (isUnothorized) {
    return (
      <ErrorState
        title="Accès refusé"
        message="Vous n'avez pas accès à cette page"
        linkText={`Retour à ${cafeName}`}
        linkTo={`/cafes/${cafeSlug}`}
      />
    );
  }

  return (
    <>
      <Helmet>
        <title>Commandes de {cafeName} | Café sans-fil</title>
      </Helmet>
      <Container className="py-10">
        <div className="mb-5 text-gray-500 font-semibold">
          <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
            <span>{cafeName}</span>
          </Link>
          <span className="px-3">&gt;</span>
          <span>Commandes</span>
        </div>
        {areOrdersLoading && (
          <div role="status" className="flex justify-center items-center h-48 w-full text-gray-500 font-semibold">
            <svg
              aria-hidden="true"
              class="w-8 h-8 text-gray-200 animate-spin fill-emerald-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg">
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        )}
        {orders.length === 0 && !areOrdersLoading && <EmptyState name="commande" genre="féminin" />}
        {orders.length > 0 &&
          orders.map((order) => (
            <CafeOrderCard
              order={order}
              setOrderReady={setOrderReady}
              setOrderCanceled={setOrderCanceled}
              key={order.order_id}
            />
          ))}
      </Container>
    </>
  );
};

export default CafeOrders;
