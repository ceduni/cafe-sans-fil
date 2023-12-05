import Container from "@/components/Container";
import CafeOrderCard from "@/components/Orders/CafeOrderCard";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { ORDER_STATUS, isPendingOrder } from "@/utils/orders";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";
import ErrorState from "@/components/ErrorState";
import useApi from "@/hooks/useApi";
import { Helmet } from "react-helmet-async";
import EmptyState from "@/components/EmptyState";
import Breadcrumbs from "@/components/Breadcrumbs";
import LoadingSpinner from "@/components/LoadingSpinner";

const CafeOrders = () => {
  const { id: cafeSlug } = useParams();

  const [orders, setOrders] = useState([]);
  const [areOrdersLoading, setAreOrdersLoading] = useState(true);
  const [isUnothorized, setIsUnauthorized] = useState(false);

  const { data, isLoading } = useApi(`/cafes/${cafeSlug}`);
  const cafeName = data?.name;

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
      <Helmet>{cafeName && <title>Commandes de {cafeName} | Café sans-fil</title>}</Helmet>
      <Container className="py-10">
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {cafeName}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Commandes</Breadcrumbs.Item>
        </Breadcrumbs>

        {areOrdersLoading && <LoadingSpinner />}
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
