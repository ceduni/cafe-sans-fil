import Container from "@/components/Container";
import CafeOrderCard from "@/components/Orders/CafeOrderCard";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const CafeOrders = () => {
  const { id } = useParams();
  const cafeSlug = id;

  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // On récupère les commandes du café
  useEffect(() => {
    const fetchOrders = async () => {
      const response = await authenticatedRequest(`/cafes/${cafeSlug}/orders`);
      setOrders(response.data);
      if (response.data.length === 0) {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, []);

  useEffect(() => {
    console.log(orders);
    if (orders.length > 0) {
      setIsLoading(false);
    }
  }, [orders]);

  return (
    <Container className="py-10">
      <div className="mb-5 text-gray-500 font-semibold">
        <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
          <span>{cafeSlug}</span>
        </Link>
        <span className="px-3">&gt;</span>
        <span>Commandes</span>
      </div>
      {isLoading && <p>Chargement...</p>}
      {orders.length === 0 && !isLoading && <p>Aucune commande pour le moment.</p>}
      {orders.length > 0 && orders.map((order) => <CafeOrderCard order={order} key={order.order_id} />)}
    </Container>
  );
};

export default CafeOrders;
