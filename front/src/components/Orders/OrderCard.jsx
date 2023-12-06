import { LoadingOrderItemCard, OrderItemCard } from "./OrderItemCard";
import Badge from "@/components/Badge";
import useCountdown from "@/hooks/useCountdown";
import { formatPrice } from "@/utils/cart";
import { ORDER_STATUS, getBadgeVariant, isPendingOrder } from "@/utils/orders";
import { formatDate } from "@/utils/dates";
import { NoSymbolIcon } from "@heroicons/react/24/outline";
import { MapPinIcon } from "@heroicons/react/24/solid";
import { displayCafeLocation } from "@/utils/cafe";

const OrderCard = ({ order, cafe, onCancel }) => {
  const minutesBeforeCancel = useCountdown(order.created_at);

  return (
    <>
      <div key={order.order_id} className="flex flex-col p-6 border border-gray-200 rounded-lg">
        <div className="flex sm:items-center sm:justify-between flex-col sm:flex-row gap-4 mb-6">
          <div className="flex items-center gap-2">
            <h3 className="text-lg text-gray-700 font-medium">Commande #{order.order_number}</h3>
            <Badge variant={getBadgeVariant(order.status)}>{order.status}</Badge>
          </div>
          {order.status === ORDER_STATUS.PLACED && (
            <div className="hidden sm:block">
              <button
                type="button"
                onClick={onCancel}
                className="inline-flex gap-2 items-center rounded-md bg-white px-3 py-2 \
              text-sm font-medium text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <NoSymbolIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                Annuler
              </button>
            </div>
          )}
        </div>

        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center">
            {(cafe.image_url && (
              <img
                className="w-12 h-12 mr-4 rounded-full object-cover"
                src={cafe.image_url}
                alt={cafe.name}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "https://placehold.co/300x300?text=:/";
                }}
              />
            )) || <div className="w-12 h-12 mr-4 rounded-full bg-gray-200 animate-pulse"></div>}
            <div>
              {(cafe.name && <h2 className="text-lg tracking-tight font-semibold text-gray-900">{cafe.name}</h2>) || (
                <div className="w-32 h-4 mb-2 rounded-full bg-gray-200 animate-pulse"></div>
              )}
              {(minutesBeforeCancel > 0 && isPendingOrder(order.status) && (
                <p className="text-sm text-gray-500" title={formatDate(order.created_at)}>
                  {minutesBeforeCancel} minutes avant annulation
                </p>
              )) || <p className="text-sm text-gray-500">{formatDate(order.created_at)}</p>}
            </div>
          </div>
          <p className="text-lg font-semibold text-gray-900">{formatPrice(order.total_price)}</p>
        </div>

        {isPendingOrder(order.status) && (
          <div className="flex items-center gap-2 mt-6">
            <MapPinIcon className="w-5 h-5 text-gray-500" />
            <p className="text-sm text-gray-500">{displayCafeLocation(cafe.location)}</p>
          </div>
        )}

        <hr className="my-6 border-gray-200" />

        <div>
          {order.items.map((item, index) => (
            <OrderItemCard item={item} key={index} />
          ))}
        </div>

        {order.status === ORDER_STATUS.PLACED && (
          <div className="sm:hidden mt-6">
            <button
              className="w-full inline-flex gap-2 items-center justify-center rounded-md bg-white \
            px-3 py-2 text-sm font-medium text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300"
              onClick={onCancel}
              type="button">
              <NoSymbolIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              Annuler
            </button>
          </div>
        )}
      </div>
    </>
  );
};

const LoadingOrderCard = () => {
  return (
    <div className="flex flex-col p-6 border border-gray-200 rounded-lg">
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

      {Array.from({ length: 3 }).map((_, index) => (
        <LoadingOrderItemCard key={index} />
      ))}
    </div>
  );
};

export { OrderCard, LoadingOrderCard };
