import { useNavigate } from "react-router-dom";
import { useCart } from "react-use-cart";
import { useAuth } from "@/hooks/useAuth";
import Container from "@/components/Layout/Container";
import {
  areItemsFromMoreThanOneCafe,
  displayCafeNames,
  formatPrice,
  displayOptions,
  optionsByTypeToArray,
} from "@/utils/cart";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";
import { useState } from "react";
import ErrorState from "@/components/Error/ErrorState";
import useTitle from "@/hooks/useTitle";
// import { Helmet } from "react-helmet-async";

const OrderConfirmation = () => {
  const { isLoggedIn } = useAuth();
  const { isEmpty, totalItems, items, cartTotal, emptyCart } = useCart();
  const [isPlacingOrder, setIsPlacingOrder] = useState(false);
  const navigate = useNavigate();

  if (isEmpty) {
    return (
      <ErrorState
        title="Votre panier est vide"
        message="Vous devez avoir au moins un item dans votre panier pour pouvoir passer une commande"
        linkText="Retourner au menu"
        linkTo="/"
      />
    );
  } else if (!isLoggedIn) {
    return (
      <ErrorState
        title="Vous devez être connecté"
        message="Vous devez être connecté pour pouvoir passer une commande"
        linkText="Se connecter"
        linkTo="/login"
      />
    );
  }

  // On va créer une commande par café
  const orders = [];
  items.forEach((item) => {
    const cafe = item.cafe;
    const order = orders.find((order) => order.cafe.cafe_id === cafe.cafe_id);
    if (order) {
      order.items.push(item);
    } else {
      orders.push({
        cafe: cafe,
        items: [item],
      });
    }
  });

  // On ajoute le total de la commande à chaque commande
  orders.forEach((order) => {
    order.total = order.items.reduce((acc, item) => acc + item.price * item.quantity, 0);
  });

  const moreThanOneCafe = areItemsFromMoreThanOneCafe(items);

  const submitOrder = async (payload) => {
    console.log("Sent order", payload);
    await authenticatedRequest.post("/orders", payload);
  };

  const placeOrder = async () => {
    setIsPlacingOrder(true);
    try {
      for (const order of orders) {
        const payload = {
          cafe_slug: order.cafe.slug,
          cafe_name: order.cafe.name,
          cafe_image_url: order.cafe.image_url,
          items: order.items.map((item) => ({
            item_name: item.name,
            item_price: item.price,
            item_slug: item.slug,
            item_image_url: item.image_url,
            options: optionsByTypeToArray(item.selectedOptions),
            quantity: item.quantity,
          })),
        };
        await submitOrder(payload);
      }
      toast.success("Votre commande a bien été passée");
      emptyCart();
      navigate("/me/orders");
    } catch (error) {
      toast.error("Une erreur est survenue lors de l'envoi de votre commande");
    } finally {
      setIsPlacingOrder(false);
    }
  };

  useTitle("Confirmation de la commande | Café sans-fil");

  return (
    <>
      <Container className="py-10">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <h2 className="text-lg leading-6 font-medium text-gray-900">Récapitulatif de la commande</h2>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                Vérifiez que tout est correct avant de valider votre commande.
              </p>
            </div>
            {orders.map((order, index) => (
              <div key={order.cafe.cafe_id}>
                <div className="border-t border-gray-200">
                  <div className="bg-gray-50 px-4 py-5 sm:px-6">
                    <span className="text-sm font-medium text-gray-500">
                      Commande {orders.length > 1 ? index + 1 : ""} chez{" "}
                      <span className="text-gray-900">{order.cafe.name}</span>
                    </span>
                  </div>
                </div>
                <ul className="divide-y divide-gray-200">
                  {order.items.map((item) => (
                    <li key={item.id}>
                      <div className="flex items-center justify-between py-4 px-4 sm:px-6">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <img
                              className="h-10 w-10 rounded-lg"
                              src={item.image_url || "https://placehold.co/300x300?text=Item"}
                              alt=""
                            />
                          </div>
                          <div className="ml-4">
                            <p className="text-sm font-medium text-gray-900">{item.name}</p>
                            <p className="text-sm text-gray-500">Quantité: {item.quantity}</p>
                            <p className="text-sm text-gray-500">{displayOptions(item.selectedOptions)}</p>
                          </div>
                        </div>
                        <div className="flex items-center">
                          <p className="text-sm text-gray-500">{formatPrice(item.price)}</p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
                <dl>
                  <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Total de la commande</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{formatPrice(order.total)}</dd>
                  </div>
                </dl>
              </div>
            ))}
            <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
              <p className="text-gray-700 font-semibold">
                Vous vous apprêtez à réserver {totalItems} {totalItems > 1 ? "items" : "item"} pour un total de{" "}
                {formatPrice(cartTotal)} à {displayCafeNames(items)}.
              </p>
              <div
                className="bg-yellow-50 border-l-4 border-yellow-400 text-orange-800 p-4 mt-4 rounded-2xl"
                role="alert">
                <h3 className="font-bold">Attention</h3>
                {moreThanOneCafe && (
                  <p className="my-3 text-sm">
                    Votre panier contient des produits de plusieurs cafés. Vous devrez récupérer plusieurs commandes,
                    une par café.
                  </p>
                )}
                <p className="text-sm">Vous aurez une heure pour récupérer votre commande. Après, elle sera annulée.</p>
              </div>
            </div>
          </div>
          <div className="mt-4 flex justify-end">
            <button
              onClick={placeOrder}
              className="inline-flex text-white bg-emerald-600 hover:bg-emerald-800 focus:ring-4 focus:outline-none focus:ring-emerald-300 font-medium rounded-3xl text-sm px-5 py-2.5 text-center">
              {isPlacingOrder ? "En cours..." : "Valider la commande"}
            </button>
          </div>
        </div>
      </Container>
    </>
  );
};

export default OrderConfirmation;
