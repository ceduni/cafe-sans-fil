import clsx from "clsx";
import { useState } from "react";

const Avatar = ({ name, size = "sm", image }) => {
  const [isImageError, setIsImageError] = useState(false);

  const words = name.split(" ");
  let initials = "";

  if (words.length > 1) {
    // Si le nom contient plus d'un mot, on prend la première lettre de chaque mot
    initials = words[0][0] + words[1][0];
  } else {
    // Sinon, on prend les deux premières lettres du mot
    initials = words[0].slice(0, 2);
  }

  initials = initials.toUpperCase();

  const sizeClasses = {
    sm: "h-8 w-8",
    md: "h-12 w-12",
    lg: "h-20 w-20",
  };

  const textClasses = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-2xl",
  };

  return (
    <div className="flex">
      {image && !isImageError ? (
        <img
          className={clsx(
            "inline-flex items-center justify-center rounded-full select-none object-cover",
            sizeClasses[size]
          )}
          src={image}
          alt={name}
          onError={() => setIsImageError(true)}
        />
      ) : (
        <span
          className={clsx(
            "inline-flex items-center justify-center rounded-full bg-gray-500 select-none",
            sizeClasses[size]
          )}>
          <span className={clsx(textClasses[size], "font-semibold leading-none text-white")}>{initials}</span>
        </span>
      )}
    </div>
  );
};

export default Avatar;
