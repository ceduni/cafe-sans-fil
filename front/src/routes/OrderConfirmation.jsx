import { Link } from "react-router-dom";
import { useCart } from "react-use-cart";
import { useAuth } from "@/hooks/useAuth";
import Container from "@/components/Container";
import { areItemsFromMoreThanOneCafe, displayCafeNames, formatPrice } from "@/utils/cart";
import InfoBox from "@/components/Cafe/InfoBox";
import Badge from "@/components/Badge";

const ErrorState = ({ title, message, linkText, linkTo }) => {
  return (
    <Container className="h-[70vh] flex flex-col justify-center">
      <div className="mx-auto max-w-screen-sm text-center">
        <p className="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl">{title}</p>
        <p className="mb-4 text-lg font-light text-gray-500">{message}</p>
        <Link
          to={linkTo}
          className="inline-flex text-white bg-emerald-600 hover:bg-emerald-800 focus:ring-4 focus:outline-none focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center my-4">
          {linkText}
        </Link>
      </div>
    </Container>
  );
};

const OrderConfirmation = () => {
  const { isLoggedIn } = useAuth();
  const { isEmpty, totalItems, items, cartTotal } = useCart();

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

  return (
    <Container className="py-10">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h2 className="text-lg leading-6 font-medium text-gray-900">Récapitulatif de la commande</h2>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Vérifiez que tout est correct avant de valider votre commande.
            </p>
          </div>
          {moreThanOneCafe && (
            <div className="mb-6 mx-auto px-4 sm:px-6">
              <Badge variant="warning">
                Vous vous apprêtez à commander des produits de plusieurs cafés. Vous devrez donc récupérer plusieurs
                commandes, une par café. Vous aurez une heure pour aller récupérer vos commandes.
              </Badge>
            </div>
          )}
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
                  <li key={item.item_id}>
                    <div className="flex items-center justify-between py-4 px-4 sm:px-6">
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <img className="h-10 w-10 rounded-lg" src="https://placehold.co/300x300?text=Item" alt="" />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{item.name}</div>
                          <div className="text-sm text-gray-500">Quantité: {item.quantity}</div>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <div className="text-sm text-gray-500">{formatPrice(item.price)}&nbsp;$</div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
              <dl>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Total de la commande</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {formatPrice(order.total)}&nbsp;$
                  </dd>
                </div>
              </dl>
            </div>
          ))}
          <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
            <p className="text-gray-700 font-semibold">
              Vous vous apprêtez à réserver {totalItems} {totalItems > 1 ? "items" : "item"} pour un total de{" "}
              {formatPrice(cartTotal)}&nbsp;$ à {displayCafeNames(items)}.
            </p>
            <InfoBox
              title="Attention"
              message="Vous aurez une heure pour aller récupérer votre commande. Au delà de ce délai, elle sera annulée."
            />
          </div>
        </div>
        <div className="mt-4 flex justify-end">
          <Link
            to=""
            className="inline-flex text-white bg-emerald-600 hover:bg-emerald-800 focus:ring-4 focus:outline-none focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
            Valider la commande
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default OrderConfirmation;
