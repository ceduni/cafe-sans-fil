import classNames from "classnames";

const Card = ({ className, children }) => {
  return (
    <div
      className={classNames(
        "overflow-hidden bg-stone-100 bg-opacity-30 rounded-lg shadow-sm border border-gray-200 flex flex-col \
        sm:hover:shadow-lg sm:transition-shadow sm:duration-300 sm:ease-in-out",
        className
      )}
      tabIndex="0">
      {children}
    </div>
  );
};

const Header = ({ className, children }) => {
  return <div className={classNames("px-4 bg-white sm:px-6 py-5 border-b border-gray-200", className)}>{children}</div>;
};

const HeaderTitle = ({ className, as = "h3", children }) => {
  const Tag = as;

  return <Tag className={classNames("text-lg font-medium leading-6 text-gray-900", className)}>{children}</Tag>;
};

const HeaderSubtitle = ({ className, as = "p", children }) => {
  const Tag = as;

  return (
    <Tag
      className={classNames("mt-1 max-w-2xl text-xs font-semibold text-gray-500", className)}
      style={{ textWrap: "pretty" }}>
      {children}
    </Tag>
  );
};

const Body = ({ className, children }) => {
  return <div className={classNames("px-3 py-4 sm:p-5 text-sm flex-grow", className)}>{children}</div>;
};

const Footer = ({ className, children }) => {
  return <div className={classNames("px-4 sm:px-6 py-5 border-t border-gray-200", className)}>{children}</div>;
};

Card.Header = Header;
Card.Header.Title = HeaderTitle;
Card.Header.Subtitle = HeaderSubtitle;
Card.Body = Body;
Card.Footer = Footer;

export default Card;
