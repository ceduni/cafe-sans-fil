const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-5">
      <div className="w-full max-w-screen-xl mx-auto p-5 md:py-8">
        <div className="flex gap-3 items-center mb-4 sm:justify-center">
          <img src="/logo_text.png" className="h-10" alt="Logo de café sans-fil" />
          <div className="flex flex-col">
            <span className="text-xl font-bold text-gray-900 font-secondary"></span>
            <span className="text-xs font-semibold text-gray-500 mt-7">(Version 0.1.0)</span>
          </div>
        </div>
        <div className="text-sm text-gray-500 sm:text-center">
          <p>
            Ceduni &bull; Projet disponible sur{" "}
            <a className="underline" href="https://github.com/ceduni/udem-cafe" target="_blank">
              GitHub
            </a>
          </p>
          <p className="mb-2">Développé par Axel ZAREB et Southidej OUDANONH</p>
          <a className="underline" href="https://github.com/ceduni/udem-cafe/issues/new" target="_blank">
            Signalez une erreur ou faites une suggestion
          </a>
          <p className="mt-3 font-semibold">&copy; 2023 Café sans-fil</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
