import { LoadingOrderItemCard, OrderItemCard } from "./OrderItemCard";
import Badge from "@/components/Badge";
import { getBadgeVariant } from "@/utils/orders";

const OrderCard = ({ order }) => {
  return (
    <>
      <div key={order.order_id} className="flex flex-col p-6 border border-gray-200 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img
              className="w-12 h-12 mr-4 rounded-full object-cover"
              src={order.cafe?.image_url || "https://placehold.co/300x300?text=..."}
              alt={order.cafe?.name}
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://placehold.co/300x300?text=:/";
              }}
            />
            <div>
              <h2 className="text-lg font-semibold text-gray-900">{order.cafe?.name}</h2>
              <p className="text-sm text-gray-500 mb-1">{order.created_at}</p>
              <Badge variant={getBadgeVariant(order.status)}>{order.status}</Badge>
            </div>
          </div>
          <p className="text-lg font-semibold text-gray-900">{order.total_price}&nbsp;$</p>
        </div>

        <hr className="my-6 border-gray-200" />

        <div>
          {order.items.map((item, index) => (
            <OrderItemCard item={item} key={index} />
          ))}
        </div>
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
