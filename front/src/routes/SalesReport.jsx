import React, { useEffect, useState, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import { formatPrice } from "@/utils/cart";
import { Helmet } from "react-helmet-async";

const SalesReport = () => {
  const { id: cafeSlug } = useParams();
  const [data, isLoading] = useApi(`/cafes/${cafeSlug}`);
  const [salesReport, setSalesReport] = useState(null);

  const fetchSalesReport = async (reportType = "daily", startDate = "", endDate = "") => {
    try {
      let url = `/cafes/${cafeSlug}/sales-report?report_type=${reportType}`;
      if (startDate) url += `&start_date=${startDate}`;
      if (endDate) url += `&end_date=${endDate}`;

      const response = await authenticatedRequest.get(url);
      setSalesReport(response.data);
    } catch (error) {
      toast.error("Erreur lors du chargement du rapport de ventes.");
    }
  };

  const today = new Date().toISOString().split("T")[0];
  const oneMonthAgo = new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split("T")[0];

  const [reportType, setReportType] = useState("daily");
  const [startDate, setStartDate] = useState(oneMonthAgo);
  const [endDate, setEndDate] = useState(today);

  useEffect(() => {
    fetchSalesReport(reportType, startDate, endDate);
  }, [cafeSlug]);

  const handleReportTypeChange = (newType) => {
    setReportType(newType);
    fetchSalesReport(newType, startDate, endDate);
  };

  if (!salesReport) {
    return (
      <div role="status" className="flex justify-center items-center h-48 w-full text-gray-500 font-semibold">
        <svg
          aria-hidden="true"
          className="w-8 h-8 text-gray-200 animate-spin fill-emerald-600"
          viewBox="0 0 100 101"
          fill="none"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="currentColor"
          />
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentFill"
          />
        </svg>
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  const findImageURL = (itemName) => {
    const menuItem = data.menu_items.find((item) => item.name === itemName);
    return menuItem ? menuItem.image_url : null;
  };

  return (
    <>
      <Helmet>{data && <title>Rapports de {data.name} | Café sans-fil</title>}</Helmet>

      <Container className="py-10">
        <div className="mb-5 text-gray-500 font-semibold">
          <Link to={`/cafes/${cafeSlug}`} className="underline underline-offset-2 hover:no-underline">
            {(isLoading && <span className="animate-pulse">Chargement...</span>) || data?.name}
          </Link>
          <span className="px-3">&gt;</span>
          <span className="text-gray-600 font-bold">Rapports de ventes</span>
        </div>

        <div className={"border-b border-gray-900/10  pb-12"}>
          <h2 className="text-base font-semibold leading-7 text-gray-900">Tendance des ventes</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Visualisez l'évolution des commandes de votre café au fil du temps. Cette section offre un aperçu graphique
            des tendances de vente.
          </p>

          <div className="mt-9 mb-2 flex justify-center">
            <div>
              <input
                className="rounded-full"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <span className="px-2">à</span>
              <input
                className="rounded-full"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>

          <div className="gap-2 flex justify-center">
            <button
              className="flex rounded-3xl bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
              onClick={() => handleReportTypeChange("daily")}>
              Quotidien
            </button>
            <button
              className="flex rounded-3xl bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
              onClick={() => handleReportTypeChange("weekly")}>
              Hebdomadaire
            </button>
            <button
              className="flex rounded-3xl bg-emerald-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
              onClick={() => handleReportTypeChange("monthly")}>
              Mensuel
            </button>
          </div>

          <div className="md:mx-16 mt-14 mb-8">
            <SalesReportChart salesTrends={salesReport.sales_trends} />
          </div>

          <div className="ml-24 text-zinc-700">
            <div>
              Total des revenus: <span className="font-semibold">{formatPrice(salesReport.total_revenue)}</span>
            </div>
            <div>
              Total des commandes: <span className="font-semibold">{salesReport.total_orders}</span>
            </div>
          </div>
        </div>

        <div className="pb-12 mt-6">
          <h2 className="text-base font-semibold leading-7 text-gray-900">Détails des ventes d'articles</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Découvrez les performances détaillées de chaque article vendu dans votre café. Cette section fournit des
            informations sur le nombre d'articles vendus et les revenus générés.
          </p>
          <ul className="divide-y divide-gray-100 mt-6">
            {salesReport.item_sales_details.map((item, index) => (
              <li
                key={index}
                className="px-6 mx-14 rounded-2xl flex flex-col sm:flex-row justify-between gap-x-6 gap-y-4 py-5">
                <div className="flex min-w-0 gap-x-4">
                  <img
                    src={findImageURL(item.item_name) || "default-placeholder-url.jpg"}
                    alt={item.item_name}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                  <div className="min-w-0 flex-auto">
                    <p className="text-sm font-semibold leading-6 text-gray-900">{item.item_name}</p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-700">
                      Vendu: <span className="font-bold">{item.item_quantity_sold}</span>
                    </p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-700">
                      Revenu: <span className="font-semibold">{formatPrice(item.item_revenue)}</span>
                    </p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </Container>
    </>
  );
};

export default SalesReport;

const SalesReportChart = ({ salesTrends }) => {
  const svgRef = useRef();
  const [svgWidth, setSvgWidth] = useState(0);
  const maxValue = Math.max(...salesTrends.map((item) => item.order_count));
  const svgHeight = 400;
  const barPadding = 1;
  const roundedCorner = 10;
  const maxLabelCount = 3;
  const interval = Math.floor(salesTrends.length / maxLabelCount);
  const leftMargin = 50;

  useEffect(() => {
    if (svgRef.current) {
      setSvgWidth(svgRef.current.parentElement.offsetWidth * 0.9);
    }
  }, []);

  const handleMouseOver = (event, item) => {
    const tooltip = document.getElementById("tooltip");
    const tooltipX = event.clientX + window.scrollX;
    const tooltipY = event.clientY + window.scrollY;

    tooltip.style.display = "block";
    tooltip.style.left = `${tooltipX}px`;
    tooltip.style.top = `${tooltipY}px`;
    tooltip.textContent = `${item.order_count} orders, ${item.time_period}`;
  };

  const handleMouseOut = () => {
    const tooltip = document.getElementById("tooltip");
    tooltip.style.display = "none";
  };

  return (
    <div>
      <svg ref={svgRef} width={svgWidth + leftMargin} height={svgHeight}>
        {/* Vertical Axis Line */}
        <line x1={leftMargin} y1="40" x2={leftMargin} y2={svgHeight - 40} stroke="black" />

        {/* Horizontal Axis Line */}
        <line x1={leftMargin} y1={svgHeight - 40} x2={svgWidth + leftMargin} y2={svgHeight - 40} stroke="black" />

        {/* Ticks and Labels for X-axis */}
        {salesTrends
          .filter((_, index) => index % interval === 0 || index === salesTrends.length - 1)
          .map((item, index) => (
            <g key={index}>
              <line
                x1={leftMargin + (index * interval * (svgWidth - leftMargin)) / salesTrends.length}
                y1={svgHeight - 40}
                x2={leftMargin + (index * interval * (svgWidth - leftMargin)) / salesTrends.length}
                y2={svgHeight - 35}
                stroke="black"
              />
              <text
                className="font-semibold"
                x={leftMargin + (index * interval * (svgWidth - leftMargin)) / salesTrends.length}
                y={svgHeight - 20}
                textAnchor="middle"
                fontSize="14px">
                {item.time_period}
              </text>
            </g>
          ))}

        {/* Ticks for Y-axis */}
        {[...Array(11)].map((_, i) => (
          <g key={i}>
            <text
              className="font-semibold"
              x={leftMargin - 25}
              y={svgHeight - 40 - (i * (svgHeight - 80)) / 10}
              fontSize="14px">
              {Math.round((maxValue * i) / 10)}
            </text>
            <line
              x1={leftMargin - 5}
              y1={svgHeight - 40 - (i * (svgHeight - 80)) / 10}
              x2={leftMargin}
              y2={svgHeight - 40 - (i * (svgHeight - 80)) / 10}
              stroke="black"
            />
          </g>
        ))}

        {/* Bars and on hover */}
        {salesTrends.map((item, index) => {
          const barWidth = (svgWidth - 30) / salesTrends.length;
          const barHeight = (item.order_count / maxValue) * (svgHeight - 80);
          return (
            <g key={index}>
              <rect
                x={leftMargin + index * barWidth + barPadding / 2}
                y={svgHeight - barHeight - 40}
                width={barWidth - barPadding}
                height={barHeight}
                fill="#3d87ea"
                rx={roundedCorner}
                ry={roundedCorner}
                onMouseOver={(e) => handleMouseOver(e, item)}
                onMouseOut={handleMouseOut}
              />
            </g>
          );
        })}
      </svg>
      <div
        id="tooltip"
        className="hidden absolute rounded-xl shadow-md bg-white text-gray-950 text-xs h-8 font-semibold w-20 text-center"
      />
    </div>
  );
};
