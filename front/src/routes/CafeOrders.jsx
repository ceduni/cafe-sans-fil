import Container from "@/components/Container";
import CafeOrderCard from "@/components/Orders/CafeOrderCard";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { ORDER_STATUS, isPendingOrder } from "@/utils/orders";
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import toast from "react-hot-toast";
import EmptyState from "@/components/EmptyState";
import useApi from "@/hooks/useApi";

const CafeOrders = () => {
  const { id } = useParams();
  const cafeSlug = id;

  const [orders, setOrders] = useState([]);
  const [areOrdersLoading, setAreOrdersLoading] = useState(true);

  const [data, isLoading] = useApi(`/cafes/${cafeSlug}`);
  const cafeName = isLoading ? "Chargement..." : data.name;

  // On récupère les commandes du café
  useEffect(() => {
    const fetchOrders = async () => {
      const response = await authenticatedRequest(`/cafes/${cafeSlug}/orders`);
      const orders = response.data.filter((order) => isPendingOrder(order.status));
      setOrders(orders);
      if (orders.length === 0) {
        setAreOrdersLoading(false);
      }
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

  return (
    <Container className="py-10">
      <div className="mb-5 text-gray-500 font-semibold">
        <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
          <span>{cafeName}</span>
        </Link>
        <span className="px-3">&gt;</span>
        <span>Commandes</span>
      </div>
      {areOrdersLoading && <p>Chargement...</p>}
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
  );
};

export default CafeOrders;
