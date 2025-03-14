import Container from "@/components/Layout/Container";
import CafeOrderCard from "@/components/Orders/CafeOrderCard";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { ORDER_STATUS, isPendingOrder } from "@/utils/orders";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";
import ErrorState from "@/components/Error/ErrorState";
import useApi from "@/hooks/useApi";
import EmptyState from "@/components/Error/EmptyState";
import Breadcrumbs from "@/components/Breadcrumbs";
import LoadingSpinner from "@/components/LoadingSpinner";
import useTitle from "@/hooks/useTitle";

const CafeOrders = () => {
  const { id: cafeSlug } = useParams();

  const [orders, setOrders] = useState([]);
  const [areOrdersLoading, setAreOrdersLoading] = useState(true);
  const [isUnothorized, setIsUnauthorized] = useState(false);
  const [refreshIndex, setRefreshIndex] = useState(0);

  const refeshOrders = () => setRefreshIndex((prev) => prev + 1);

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
  }, [refreshIndex]);

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
    authenticatedRequest
      .put(`/orders/${orderId}`, payload)
      .then((response) => {
        if (newStatus === ORDER_STATUS.COMPLETED) {
          toast.success("Commande complétée!");
        } else if (newStatus === ORDER_STATUS.CANCELED) {
          toast.success("Commande annulée!");
        }
      })
      .catch((error) => {
        toast.error("Erreur lors de la mise à jour de la commande");
      })
      .finally(() => {
        toast.dismiss(toastId);
        refeshOrders();
      });
  };

  const setOrderReady = (orderId) => {
    updateOrderStatus(orderId, ORDER_STATUS.READY);
  };
  const setOrderCompleted = (orderId) => {
    updateOrderStatus(orderId, ORDER_STATUS.COMPLETED);
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

  useTitle(`Commandes de ${cafeName} | Café sans-fil`);

  return (
    <>
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
              setOrderCompleted={setOrderCompleted}
              setOrderCanceled={setOrderCanceled}
              key={order.order_id}
            />
          ))}
      </Container>
    </>
  );
};

export default CafeOrders;
