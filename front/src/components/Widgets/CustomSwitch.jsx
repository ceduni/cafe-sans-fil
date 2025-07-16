import { Switch } from "@headlessui/react";
import clsx from "clsx";

const CustomSwitch = ({ checked, onChange, label = null }) => {
  return (
    <Switch.Group as="div" className="flex items-center">
      <Switch
        checked={checked}
        onChange={onChange}
        className={clsx(
          checked ? "bg-emerald-600" : "bg-gray-200",
          "relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-sky-500"
        )}>
        <span
          aria-hidden="true"
          className={clsx(
            checked ? "translate-x-5" : "translate-x-0",
            "pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"
          )}
        />
      </Switch>
      {label && (
        <Switch.Label as="span" className="ml-3 text-sm font-medium text-gray-700">
          {label}
        </Switch.Label>
      )}
    </Switch.Group>
  );
};

export default CustomSwitch;
