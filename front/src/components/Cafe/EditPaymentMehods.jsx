import { PAYMENT_METHODS } from "@/utils/cafe";
import { useState } from "react";
import Input from "@/components/Input";
import Switch from "../CustomSwitch";
import classNames from "classnames";

const EditPaymentMethods = ({ cafeData, setCafeData }) => {
  const isPaymentMethodAccepted = (method) => {
    return cafeData?.payment_methods.some((m) => m.method === PAYMENT_METHODS[method]);
  };

  const getPaymentMethodMin = (method) => {
    return cafeData?.payment_methods.find((m) => m.method === PAYMENT_METHODS[method])?.minimum;
  };

  return (
    <div className="mt-6">
      {Object.keys(PAYMENT_METHODS).map((method) => (
        <div key={method} className="py-6">
          <div className="flex justify-between">
            <p className="font-medium">{PAYMENT_METHODS[method]}</p>
            <p
              className={classNames("text-sm", {
                "text-green-500": isPaymentMethodAccepted(method),
              })}>
              {isPaymentMethodAccepted(method) ? "Accepté" : "Non accepté"}
            </p>
          </div>
          <p className="text-sm text-gray-500">
            {isPaymentMethodAccepted(method)
              ? PAYMENT_METHODS[method] === PAYMENT_METHODS.CASH
                ? "Pas de minimum pour le paiement en argent comptant."
                : `Minimum de ${getPaymentMethodMin(method)}$ avec ${PAYMENT_METHODS[method]}.`
              : null}
          </p>
          {PAYMENT_METHODS[method] !== PAYMENT_METHODS.CASH && (
            <div className="space-y-2 mt-6">
              <label htmlFor={`payment_methods_${method}_min`} className="block text-sm font-medium text-gray-700">
                Minimum
              </label>
              <Input id={`payment_methods_${method}_min`} name="min" type="number" step="0.01" />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default EditPaymentMethods;
