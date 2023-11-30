import { Children, Fragment } from "react";
import { Link } from "react-router-dom";

const Breadcrumbs = ({ children }) => {
  const arrayChildren = Children.toArray(children);

  return (
    <div className="mb-5 text-gray-500 font-semibold text-sm sm:text-base">
      {arrayChildren.map((child, index) => {
        const isLast = index === arrayChildren.length - 1;

        if (isLast) {
          return (
            <span key={index} className="text-gray-600 font-bold">
              {child}
            </span>
          );
        }

        return (
          <Fragment key={index}>
            {child}
            <span className="px-3">&gt;</span>
          </Fragment>
        );
      })}
    </div>
  );
};

const Item = ({ link, children }) => {
  return link ? (
    <Link to={link} className="underline underline-offset-2 hover:no-underline">
      {children}
    </Link>
  ) : (
    <>{children}</>
  );
};

Breadcrumbs.Item = Item;

export default Breadcrumbs;
