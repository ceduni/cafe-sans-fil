import { displayOptions, formatPrice, getAdditionalPriceFromOptions } from "@/utils/cart";

const OrderItemCard = ({ item }) => {
  return (
    <div className="mb-6 last:mb-0">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <img
            className="w-8 h-8 mr-4 rounded-lg object-cover"
            src={item.item_image_url || "https://placehold.co/300x300?text=Item"}
            alt={item.item_name}
          />
          <div>
            <div className="flex items-center gap-1">
              <span className="text-gray-800 text-sm bg-gray-200 rounded px-2">{item.quantity}</span>
              <h3 className="text-base font-semibold text-gray-900">{item.item_name}</h3>
            </div>
            {item.quantity > 1 && <p className="text-sm text-gray-500">{formatPrice(item.item_price)} l'unité</p>}
          </div>
        </div>
        <p className="text-base font-semibold text-gray-900">{formatPrice(item.item_price * item.quantity)}</p>
      </div>
      {item.options.length > 0 && (
        <div className="flex items-center justify-between mt-3">
          <p className="text-sm text-gray-500">+&nbsp;{displayOptions(item.options)}</p>
          {(getAdditionalPriceFromOptions(item.options) > 0 && (
            <p>+{formatPrice(getAdditionalPriceFromOptions(item.options) * item.quantity)}</p>
          )) || <p className="text-gray-500">Gratuit</p>}
        </div>
      )}
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
