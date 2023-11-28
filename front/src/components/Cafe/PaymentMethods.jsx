import { formatPrice } from "@/utils/cart";
import { BanknotesIcon, CreditCardIcon, EllipsisHorizontalCircleIcon } from "@heroicons/react/24/solid";

const PaymentMethods = ({ arrayOfMethods }) => {
  const iconClassName = "h-4 w-4 text-gray-500";

  const icon = {
    "Carte de crédit": <CreditCardIcon className={iconClassName} />,
    "Argent comptant": <BanknotesIcon className={iconClassName} />,
    "Carte de débit": <CreditCardIcon className={iconClassName} />,
  };

  return (
    <div>
      <div className="flex gap-x-3 flex-wrap">
        {arrayOfMethods.map((m, index) => (
          <div key={index} className="flex items-center gap-x-1">
            {icon[m.method] || <EllipsisHorizontalCircleIcon className={iconClassName} />}
            <p className="text-gray-500">
              {m.method} <span className="font-semibold">{m.minimum && `(min ${formatPrice(m.minimum)})`}</span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PaymentMethods;
