import { Outlet } from "react-router-dom";
import Navbar from "@/components/Layout/Navbar";
import ScrollToTop from "@/helpers/ScrollToTop";
import { AuthProvider } from "@/hooks/useAuth";
import { Toaster } from "react-hot-toast";
import Footer from "@/components/Layout/Footer";
import { CartProvider } from "react-use-cart";

const PageWrapper = () => {
    return (
        <AuthProvider>
            <CartProvider>
                <ScrollToTop />
                <Navbar />
                <div id="content">
                    <Outlet />
                </div>
                <Footer />
                <Toaster position="bottom-right" />
            </CartProvider>
        </AuthProvider>
    );
};

export default PageWrapper;
