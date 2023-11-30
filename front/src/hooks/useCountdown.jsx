import { useState, useEffect } from "react";
import dayjs from "dayjs";
import { UTCToMontrealTime } from "@/utils/dates";

// Renvoie le nombre de minutes restantes avant que la commande ne soit annulée
const useCountdown = (orderCreatedAt) => {
  const [minutes, setMinutes] = useState(0);
  const orderDate = dayjs(UTCToMontrealTime(orderCreatedAt));
  const orderDatePlusOneHour = orderDate.add(1, "hour").valueOf();

  const getMinutes = () => {
    const now = dayjs();
    const minutes = dayjs(orderDatePlusOneHour).diff(now, "minute");
    return minutes;
  };

  useEffect(() => {
    setMinutes(getMinutes());
    const interval = setInterval(() => {
      setMinutes(getMinutes());
    }, 60000);
    return () => clearInterval(interval);
  }, []);

  return minutes;
};

export default useCountdown;
