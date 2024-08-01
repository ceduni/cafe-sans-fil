import classNames from "classnames";


export const Container = ({ children, className, bare = false }) => {
  if (bare) {
    return <div className={className}>{children}</div>;
  }
  return <div className={classNames("px-4 sm:px-6 lg:px-8", className)}>{children}</div>;
};

export default Container;