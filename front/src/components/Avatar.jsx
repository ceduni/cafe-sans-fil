import classNames from "classnames";

const Avatar = ({ name, size = "md" }) => {
  const words = name.split(" ");
  let initials = "";

  if (words.length > 1) {
    // Si le nom contient plus d'un mot, on prend la première lettre de chaque mot
    initials = words[0][0] + words[1][0];
  } else {
    // Sinon, on prend les deux premières lettres du mot
    initials = words[0].slice(0, 2);
  }

  return (
    <div className="flex">
      <span
        className={classNames(
          "inline-flex items-center justify-center rounded-full bg-gray-500 select-none",
          size === "lg" ? "h-20 w-20" : "h-8 w-8"
        )}>
        <span className={classNames(size === "lg" ? "text-2xl" : "text-xs", "font-semibold leading-none text-white")}>
          {initials}
        </span>
      </span>
    </div>
  );
};

export default Avatar;
