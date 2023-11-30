import classNames from "classnames";

const Badge = ({ children, variant = "neutral", size = "sm" }) => {
  const colors = {
    neutral: "bg-gray-100 text-gray-600 ring-gray-500/10",
    success: "bg-green-100 text-green-700 ring-green-600/20",
    danger: "bg-red-100 text-red-700 ring-red-600/10",
    warning: "bg-yellow-100 text-yellow-800 ring-yellow-600/20",
    info: "bg-blue-100 text-blue-700 ring-blue-700/10",
  };

  const sizes = {
    sm: "px-2 py-1 text-xs",
    md: "px-3 py-1.5 text-sm",
    lg: "px-4 py-2 text-base",
  };

  return (
    <span
      className={classNames(
        "inline-flex items-center font-medium rounded-md ring-1 ring-inset",
        colors[variant],
        sizes[size]
      )}>
      {children}
    </span>
  );
};

export default Badge;
