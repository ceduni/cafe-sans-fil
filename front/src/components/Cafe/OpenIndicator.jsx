import { isCafeActuallyOpen } from "@/utils/cafe";
import classNames from "classnames";

const OpenIndicator = ({ isOpen, openingHours, size = "sm" }) => {
  const isActuallyOpen = isCafeActuallyOpen(isOpen, openingHours);
  const text = isActuallyOpen ? "Ouvert" : isOpen ? "Fermé" : "Fermé exceptionnellement";

  return (
    <div className={classNames("flex items-center gap-x-1.5", size === "sm" ? "py-3" : "mt-2")}>
      <div className={classNames("flex-none rounded-full p-1", isActuallyOpen ? "bg-emerald-500/20" : "")}>
        <div className={classNames("h-3 w-3 rounded-full", isActuallyOpen ? "bg-emerald-500" : "bg-red-500")} />
      </div>
      <p
        className={classNames(
          "text-gray-500",
          size === "sm" ? "text-sm leading-5 font-semibold" : "text-xs leading-4 font-medium"
        )}>
        {text}
      </p>
    </div>
  );
};

export default OpenIndicator;
