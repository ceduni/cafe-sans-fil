import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ScrollToTop from "../helpers/ScrollToTop";

const NavbarWrapper = () => {
  return (
    <>
      <ScrollToTop />
      <Navbar />
      <div id="content">
        <Outlet />
      </div>
    </>
  );
};

export default NavbarWrapper;
