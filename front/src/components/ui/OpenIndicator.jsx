import classNames from "classnames";

const OpenIndicator = ({ isOpen }) => {
  return (
    <div className="my-3 flex items-center gap-x-1.5">
      <div className={classNames("flex-none rounded-full p-1", isOpen ? "bg-emerald-500/20" : "bg-red-500/20")}>
        <div className={classNames("h-3 w-3 rounded-full", isOpen ? "bg-emerald-500" : "bg-red-500")} />
      </div>
      <p className="text-sm leading-5 text-gray-500 font-semibold">{isOpen ? "Ouvert" : "Fermé"}</p>
    </div>
  );
};

export default OpenIndicator;
