import { BanknotesIcon, CreditCardIcon, EllipsisHorizontalCircleIcon } from "@heroicons/react/24/solid";

const PaymentMethods = ({ arrayOfMethods }) => {
  const iconClassName = "h-4 w-4 text-gray-500";

  const text = { "Credit Card": "Carte de crédit", Cash: "Argent comptant", "Debit Card": "Carte de débit" };
  const icon = {
    "Credit Card": <CreditCardIcon className={iconClassName} />,
    Cash: <BanknotesIcon className={iconClassName} />,
    "Debit Card": <CreditCardIcon className={iconClassName} />,
  };

  return (
    <div>
      <div className="flex gap-x-3 flex-wrap">
        {arrayOfMethods.map((m, index) => (
          <div key={index} className="flex items-center gap-x-1">
            {icon[m.method] || <EllipsisHorizontalCircleIcon className={iconClassName} />}
            <p className="text-gray-500">
              {text[m.method] || m.method} (min ${m.minimum})
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PaymentMethods;
