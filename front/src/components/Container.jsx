import classNames from "classnames";

const Container = ({ children, className }) => {
  return <div className={classNames("mx-auto px-4 sm:px-6 lg:px-8", className)}>{children}</div>;
};

export default Container;
