import CardPaymentIcon from "@/assets/icons/card-payment-icon.svg";

const PaymentType = ({ name, container: Container = 'div' }) => {
    return (
        <Container className="accepted-payment">
            <img className="accepted-payment-icon" src={CardPaymentIcon} alt="Payment icon" />
            <p className="bare accepted-payment-text">{name}</p>
        </Container>
    );
};

export default PaymentType;
