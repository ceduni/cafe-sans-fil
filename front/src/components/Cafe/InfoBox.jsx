import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import classNames from "classnames";

const InfoBox = ({ title, message, className }) => {
  return (
    <div
      className={classNames(
        "border-stroke flex items-center rounded-md border border-l-[8px] border-l-sky-300 bg-white p-5 pl-8",
        className
      )}>
      <div className="mr-5 flex h-[36px] w-full max-w-[36px] items-center justify-center rounded-lg bg-sky-300">
        <ExclamationCircleIcon className="h-6 w-6 text-white" />
      </div>
      <div className="flex w-full items-center justify-between">
        <div>
          <h3 className="mb-1 text-lg font-medium text-black">{title}</h3>
          <p className="text-body-color text-sm">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default InfoBox;
