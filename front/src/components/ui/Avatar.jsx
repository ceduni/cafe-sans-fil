const Avatar = ({ name }) => {
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
      <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-gray-500 select-none">
        <span className="text-sm font-semibold leading-none text-white">{initials}</span>
      </span>
    </div>
  );
};

export default Avatar;
