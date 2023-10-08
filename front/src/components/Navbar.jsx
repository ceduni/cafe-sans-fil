import React from "react";
import { BrowserRouter, Route, Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Accueil</Link>
        </li>
        <li>
          <Link to="/login">Login</Link>
        </li>
        <li>
          <Link to="/page-inconnue">Page inconnue</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
