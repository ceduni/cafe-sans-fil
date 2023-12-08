import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import toast from "react-hot-toast";
import Container from "@/components/Container";
import useApi from "@/hooks/useApi";
import { formatPrice } from "@/utils/cart";
import { Helmet } from "react-helmet-async";
import Breadcrumbs from "@/components/Breadcrumbs";
import AdminOnly from "@/helpers/AdminOnly";
import { isAdmin } from "@/utils/admin";
import { useAuth } from "@/hooks/useAuth";
import LoadingSpinner from "@/components/LoadingSpinner";

const SalesReport = () => {
  const { id: cafeSlug } = useParams();
  const { data, isLoading, error } = useApi(`/cafes/${cafeSlug}`);
  const [salesReport, setSalesReport] = useState(null);
  const { user } = useAuth();

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

  const buttonBaseClass =
    "flex rounded-3xl px-3 py-1.5 text-sm font-semibold leading-6 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2";
  const buttonNormalClass = `${buttonBaseClass} bg-emerald-600 text-white hover:bg-emerald-500 focus-visible:outline-emerald-600`;
  const buttonSelectedClass = `${buttonBaseClass} bg-emerald-700 text-white`;

  useEffect(() => {
    if (isAdmin(data, user?.username)) {
      fetchSalesReport(reportType, startDate, endDate);
    }
  }, [data, user, reportType, startDate, endDate]);

  const handleReportTypeChange = (newType) => {
    setReportType(newType);
    fetchSalesReport(newType, startDate, endDate);
  };

  if (!salesReport) {
    return (
      <AdminOnly cafe={data} error={error}>
        <LoadingSpinner />
      </AdminOnly>
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
        <Breadcrumbs>
          <Breadcrumbs.Item link="/">Cafés</Breadcrumbs.Item>
          <Breadcrumbs.Item link={`/cafes/${cafeSlug}`} isLoading={isLoading}>
            {data?.name}
          </Breadcrumbs.Item>
          <Breadcrumbs.Item>Rapports de ventes</Breadcrumbs.Item>
        </Breadcrumbs>

        <div className={"border-b border-gray-900/10  pb-12"}>
          <h2 className="text-base font-semibold leading-7 text-gray-900">Tendance des ventes</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            Visualisez l'évolution des commandes de votre café au fil du temps. Cette section offre un aperçu graphique
            des tendances de vente.
          </p>

          <div className="mt-7 sm:mt-9 mb-2 flex justify-center">
            <div className="mb-3 sm:mb-1">
              <input
                className="px-2 rounded-full"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <span className="px-2">à</span>
              <input
                className="px-2 rounded-full"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>

          <div className="gap-2 flex justify-center">
            <button
              className={reportType === "daily" ? buttonSelectedClass : buttonNormalClass}
              onClick={() => handleReportTypeChange("daily")}>
              Quotidien
            </button>
            <button
              className={reportType === "weekly" ? buttonSelectedClass : buttonNormalClass}
              onClick={() => handleReportTypeChange("weekly")}>
              Hebdomadaire
            </button>
            <button
              className={reportType === "monthly" ? buttonSelectedClass : buttonNormalClass}
              onClick={() => handleReportTypeChange("monthly")}>
              Mensuel
            </button>
          </div>

          <div className="xl:grid xl:grid-cols-2 :mx-16 mt-14 mb-8">
            <div>
              <SalesReportChart
                salesTrends={salesReport.sales_revenue_trends}
                valueExtractor={(item) => item.total_revenue || 0}
                label={(item) => `${formatPrice(item.total_revenue)}`}
              />
              <div className="mt-2 ml-32 sm:ml-48 text-zinc-700">
                Total des revenus: <span className="font-semibold">{formatPrice(salesReport.total_revenue)}</span>
              </div>
            </div>
            <div>
              <SalesReportChart
                salesTrends={salesReport.sales_order_trends}
                valueExtractor={(item) => item.order_count || 0}
                label={(item) => `${item.order_count || 0} orders`}
              />
              <div className="mt-2 ml-32 sm:ml-48 text-zinc-700">
                Total des commandes: <span className="font-semibold">{salesReport.total_orders}</span>
              </div>
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
                className="px-2 rounded-2xl flex flex-col sm:flex-row justify-between gap-x-6 gap-y-4 py-5">
                <div className="flex min-w-0 gap-x-4">
                  <img
                    src={findImageURL(item.item_name) || "https://placehold.co/300x300?text=:/"}
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

const SalesReportChart = ({ salesTrends, valueExtractor, label }) => {
  const svgRef = useRef();
  const [svgWidth, setSvgWidth] = useState(0);
  const maxValue = Math.max(...salesTrends.map(valueExtractor), 1);
  const svgHeight = 400;
  const barPadding = 1;
  const roundedCorner = 10;
  const maxLabelCount = 3;
  const interval = Math.floor(salesTrends.length / maxLabelCount);
  const leftMargin = 50;

  const upperLimitForTicks = 10;
  const numberOfTicks = Math.min(maxValue, upperLimitForTicks);

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
    tooltip.textContent = `${label(item)}, ${item.time_period}`;
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
              y={svgHeight - 40 - (i * (svgHeight - 80)) / numberOfTicks}
              fontSize="14px">
              {Math.round((maxValue * i) / numberOfTicks)}
            </text>
            <line
              x1={leftMargin - 5}
              y1={svgHeight - 40 - (i * (svgHeight - 80)) / numberOfTicks}
              x2={leftMargin}
              y2={svgHeight - 40 - (i * (svgHeight - 80)) / numberOfTicks}
              stroke="black"
            />
          </g>
        ))}

        {/* Bars and on hover */}
        {salesTrends.map((item, index) => {
          const barWidth = Math.max((svgWidth - 30) / salesTrends.length, 1);
          const value = valueExtractor(item);
          const barHeight = (value / maxValue) * (svgHeight - 80);
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
