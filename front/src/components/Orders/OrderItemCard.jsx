import { formatPrice } from "@/utils/cart";

const OrderItemCard = ({ item }) => {
  return (
    <div className="flex items-center justify-between mb-6 last:mb-0">
      <div className="flex items-center">
        <img
          className="w-8 h-8 mr-4 rounded-lg object-cover"
          src={item.itemData?.image_url || "https://placehold.co/300x300?text=Item"}
          alt={item.itemData?.name}
        />
        <div>
          <h3 className="text-base font-semibold text-gray-900">{item.itemData?.name}</h3>
          <p className="text-sm text-gray-500">
            Quantité: {item.quantity} ({item.itemData?.price}&nbsp;$ l'unité)
          </p>
        </div>
      </div>
      <p className="text-base font-semibold text-gray-900">
        {formatPrice(item.itemData?.price * item.quantity)}&nbsp;$
      </p>
    </div>
  );
};

const LoadingOrderItemCard = () => {
  return (
    <div className="flex items-center justify-between mb-6 last:mb-0">
      <div className="flex items-center">
        <div className="w-8 h-8 mr-4 rounded-lg bg-gray-200 animate-pulse"></div>
        <div>
          <div className="w-32 h-4 mb-2 rounded-full bg-gray-200 animate-pulse"></div>
          <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
        </div>
      </div>
      <div className="w-16 h-3 rounded-full bg-gray-200 animate-pulse"></div>
    </div>
  );
};

export { OrderItemCard, LoadingOrderItemCard };