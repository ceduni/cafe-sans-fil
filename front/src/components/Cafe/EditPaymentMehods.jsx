import { PAYMENT_METHODS } from "@/utils/cafe";
import { useEffect, useState } from "react";
import Input from "@/components/Input";
import Switch from "@/components/CustomSwitch";

const EditPaymentMethods = ({ cafeData, setCafeData }) => {
  const allPaymentMethods = Object.values(PAYMENT_METHODS);

  const [isMethodSupported, setIsMethodSupported] = useState({});
  useEffect(() => {
    if (!cafeData) return;
    const newIsMethodSupported = {};
    allPaymentMethods.forEach((method) => {
      newIsMethodSupported[method] = cafeData.payment_methods.some((pm) => pm.method === method);
    });
    setIsMethodSupported(newIsMethodSupported);
  }, [cafeData]);

  const handleMinimumChange = (method, value) => {
    const newCafeData = { ...cafeData };
    const paymentMethods = newCafeData.payment_methods;
    const paymentMethod = paymentMethods.find((pm) => pm.method === method);
    let newValue = value;
    if (value === "") newValue = null;
    paymentMethod.minimum = newValue;
    setCafeData(newCafeData);
  };

  const enableMethod = (method) => {
    const newCafeData = { ...cafeData };
    const paymentMethods = newCafeData.payment_methods;
    if (!paymentMethods.some((pm) => pm.method === method)) {
      paymentMethods.push({ method, minimum: null });
      setCafeData(newCafeData);
    }
  };
  const disableMethod = (method) => {
    const newCafeData = { ...cafeData };
    const paymentMethods = newCafeData.payment_methods;
    const index = paymentMethods.findIndex((pm) => pm.method === method);
    if (index >= 0) {
      paymentMethods.splice(index, 1);
      setCafeData(newCafeData);
    }
  };

  return (
    <div className="mt-6">
      {allPaymentMethods.map((method) => (
        <div key={method} className="py-6">
          <div className="flex justify-between">
            <p className="text-base text-gray-700">{method}</p>
            <Switch
              checked={isMethodSupported[method] || false}
              onChange={(e) => (e ? enableMethod(method) : disableMethod(method))}
            />
          </div>
          {method !== PAYMENT_METHODS.CASH && isMethodSupported[method] && (
            <div className="space-y-2 mt-3">
              <label htmlFor={`payment_methods_${method}_min`} className="block text-sm font-medium text-gray-500">
                Montant minimum requis <span className="text-xs text-gray-500">(optionnel)</span>
              </label>
              <Input
                id={`payment_methods_${method}_min`}
                name="min"
                type="number"
                min="0"
                max="1000"
                step="0.01"
                value={cafeData?.payment_methods.find((pm) => pm.method === method)?.minimum || ""}
                onChange={(e) => handleMinimumChange(method, e.target.value)}
              />
              <p className="mt-2 text-sm text-gray-500">Laisser vide pour aucun minimum.</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default EditPaymentMethods;
