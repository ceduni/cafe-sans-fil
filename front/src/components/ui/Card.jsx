import classNames from "classnames";

const Card = ({ className, children }) => {
  return (
    <div className={classNames("overflow-hidden bg-white rounded-lg shadow-sm border", className)}>{children}</div>
  );
};

const Header = ({ className, children }) => {
  return <div className={classNames("px-4 sm:px-6 py-5 bg-white border-b border-gray-200", className)}>{children}</div>;
};

const HeaderTitle = ({ className, as = "h3", children }) => {
  const Tag = as;

  return <Tag className={classNames("text-lg font-medium leading-6 text-gray-900", className)}>{children}</Tag>;
};

const Body = ({ className, children }) => {
  return <div className={classNames("px-4 py-5 sm:p-6", className)}>{children}</div>;
};

const Footer = ({ className, children }) => {
  return (
    <div className={classNames("px-4 sm:px-6 py-5 bg-white border-t border-gray-200 ", className)}>{children}</div>
  );
};

Card.Header = Header;
Card.Header.Title = HeaderTitle;
Card.Body = Body;
Card.Footer = Footer;

export default Card;
