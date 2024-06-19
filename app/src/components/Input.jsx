import classNames from "classnames";

const Input = ({ className, ...props }) => {
  return (
    <input
      {...props}
      className={classNames(
        "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 \
        placeholder:text-gray-400 \
        focus:ring-2 focus:ring-inset focus:ring-sky-600 focus:ring-opacity-75 \
        sm:text-sm sm:leading-6 \
        focus:invalid:border-red-600 focus:invalid:ring-red-600 focus:invalid:ring-opacity-70\
        disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none",
        className
      )}
    />
  );
};

export default Input;
