const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 py-5">
      <div className="w-full max-w-screen-xl mx-auto p-5 md:py-8">
        <div className="flex gap-3 items-center mb-4 justify-center">
          <img src="/logo_text.png" className="h-10" alt="Logo de café sans-fil" />
        </div>
        <div className="text-sm text-gray-500 text-center space-y-3">
          <span className="font-semibold">Version {APP_VERSION}</span>
          <div>
            <p>
              Ceduni &bull; Projet disponible sur{" "}
              <a className="underline" href="https://github.com/ceduni/udem-cafe" target="_blank">
                GitHub
              </a>
            </p>
            <p>Développé par Axel ZAREB et Southidej OUDANONH</p>
          </div>
          <a className="underline block" href="https://github.com/ceduni/udem-cafe/issues/new" target="_blank">
            Signalez une erreur ou faites une suggestion
          </a>
          <p className="font-semibold">&copy; 2023 Café sans-fil</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
