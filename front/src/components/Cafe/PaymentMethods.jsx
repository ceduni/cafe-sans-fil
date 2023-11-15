import { BanknotesIcon, CreditCardIcon, EllipsisHorizontalCircleIcon } from "@heroicons/react/24/solid";

const PaymentMethods = ({ arrayOfMethods }) => {
  const iconClassName = "h-4 w-4 text-gray-500";

  const icon = {
    "Carte de crédit": <CreditCardIcon className={iconClassName} />,
    Espèces: <BanknotesIcon className={iconClassName} />,
    Chèque: <BanknotesIcon className={iconClassName} />,
    "Carte de débit": <CreditCardIcon className={iconClassName} />,
  };

  return (
    <div>
      <div className="flex gap-x-3 flex-wrap">
        {arrayOfMethods.map((m, index) => (
          <div key={index} className="flex items-center gap-x-1">
            {icon[m.method] || <EllipsisHorizontalCircleIcon className={iconClassName} />}
            <p className="text-gray-500">
              {m.method} {m.minimum && `(min ${m.minimum} $)`}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PaymentMethods;
