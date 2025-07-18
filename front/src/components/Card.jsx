import clsx from "clsx";

const Card = ({ className, children, onClick }) => {
  return (
    <div
      className={clsx(
        "overflow-hidden focus:outline-none bg-[#fdfdfd] rounded-3xl sm:rounded-[1.25rem] shadow-sm border border-gray-200 flex flex-col group\
        sm:hover:shadow-lg sm:transition-shadow sm:duration-300 sm:ease-in-out hover:animate-scale",
        className
      )}
      tabIndex="0"
      onClick={onClick}>
      {children}
    </div>
  );
};

const Image = ({ className, src, alt }) => {
  return <img className={clsx("w-full h-48 sm:h-[10.20rem] object-cover group-hover:rounded-none group-hover:scale-[1.02] duration-200", className)} src={src} alt={alt} />;
};

const Header = ({ className, children }) => {
  return <div className={clsx("px-4 sm:px-6 py-5", className)}>{children}</div>;
};

const HeaderTitle = ({ className, as = "h3", children }) => {
  const Tag = as;

  return <Tag className={clsx("text-lg font-semibold tracking-tight leading-6 ", className)}>{children}</Tag>;
};

const HeaderSubtitle = ({ className, as = "p", children }) => {
  const Tag = as;

  return (
    <Tag
      className={clsx("mt-1 max-w-2xl text-xs font-semibold text-gray-500", className)}
      style={{ textWrap: "pretty" }}>
      {children}
    </Tag>
  );
};

const Body = ({ className, children }) => {
  return <div className={clsx("px-3 py-4 sm:p-5 text-sm flex-grow", className)}>{children}</div>;
};

const Footer = ({ className, children }) => {
  return <div className={clsx("px-4 sm:px-6 pb-5", className)}>{children}</div>;
};

Card.Image = Image
Card.Header = Header;
Card.Header.Title = HeaderTitle;
Card.Header.Subtitle = HeaderSubtitle;
Card.Body = Body;
Card.Footer = Footer;

export default Card;
