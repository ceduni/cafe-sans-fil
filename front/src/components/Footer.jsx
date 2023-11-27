const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-5">
      <div className="w-full max-w-screen-xl mx-auto p-5 md:py-8">
        <div className="text-sm text-gray-500 sm:text-center">
          <span className="block sm:inline-block sm:mr-4 mb-2 sm:mb-0 font-bold">Preview v0.1.0</span>
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
