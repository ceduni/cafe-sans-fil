import 'dart:ffi';

import 'package:app/provider/order_provider.dart';
import 'package:app/provider/stock_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/widgets/Color%20list%20chart/color_list_chart.dart';
import 'package:app/widgets/alert_notification_widget.dart';
import 'package:app/widgets/histogram/custom_bar_chart.dart';
import 'package:app/widgets/Date%20selector/year_picker_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  @override
  void initState() {
    super.initState();
    fetch();
  }

  Future<void> fetch() async {
    await context.read<OrderProvider>().fetchOrders();
    if (!mounted) return;

    await context.read<StockProvider>().fetchStock();
    if (!mounted) return;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        drawer: const Sidebar(),
        appBar: AppBar(
          title: Text(AppLocalizations.of(context)!.pagesTitles_dashboardTitle),
          surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
        ),
        body: Consumer2<OrderProvider, StockProvider>(
            builder: (context, orderProvider, stockProvider, child) {
          if (orderProvider.isLoading || stockProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (orderProvider.hasError || stockProvider.hasError) {
            return Center(
                child: Text(
                    'Error: ${orderProvider.errorMessage ?? stockProvider.errorMessage}'));
          } else {
            return SingleChildScrollView(
              child: Column(
                children: [
                  Center(
                    // ----------- logo ------------
                    child: ClipRect(
                      child: SizedBox(
                        height: 150,
                        width: 150,
                        child: Image.asset(
                          'images/logo.png',
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),
                  ),
                  // ----------- Notification ------------
                  Container(
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: AlertNotificationWidget(
                        listOfProductsName: context
                            .watch<StockProvider>()
                            .lowStockProcductName),
                  ),

                  // ----------- Turnover ------------
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.lightBlue[100],
                              borderRadius: BorderRadius.circular(10),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.grey.withOpacity(0.5),
                                  spreadRadius: 5,
                                  blurRadius: 7,
                                  offset: const Offset(0, 3),
                                ),
                              ],
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  AppLocalizations.of(context)!.turnover_text,
                                  style: const TextStyle(
                                    fontSize: 15.0,
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                  ),
                                  softWrap: true,
                                ),
                                const SizedBox(height: 10.0),
                                // -- turnover value --
                                Text(
                                  '${context.watch<OrderProvider>().turnOver.toStringAsFixed(2)} CAD',
                                  style: const TextStyle(
                                    fontSize: 20.0,
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                  ),
                                )
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        // ----------- Profit ------------
                        Expanded(
                          child: Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: Colors.lightBlue[100],
                              borderRadius: BorderRadius.circular(10),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.grey.withOpacity(0.5),
                                  spreadRadius: 5,
                                  blurRadius: 7,
                                  offset: const Offset(0, 3),
                                ),
                              ],
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  AppLocalizations.of(context)!.profits_text,
                                  style: const TextStyle(
                                    fontSize: 15,
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                  ),
                                  softWrap: true,
                                ),
                                const SizedBox(height: 10.0),
                                // -- profit value --
                                Text(
                                  '${context.watch<OrderProvider>().profit.toStringAsFixed(2)} CAD',
                                  style: const TextStyle(
                                    fontSize: 20.0,
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20.0),
                  // -------------------Date selector------------------------------
                  Container(
                    alignment: Alignment.center,
                    width: MediaQuery.of(context).size.width * 0.9,
                    padding: const EdgeInsets.symmetric(vertical: 8.0),
                    decoration: BoxDecoration(
                      color: const Color.fromARGB(255, 138, 199, 249),
                      borderRadius: BorderRadius.circular(30),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        Text(
                          AppLocalizations.of(context)!.choose_period,
                          style: const TextStyle(color: Colors.white),
                        ),
                        // const PeriodSelector(),
                        YearPickerWidget(),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20.0),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: Container(
                      padding: const EdgeInsets.all(16),
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: Colors.lightBlue[100],
                        borderRadius: BorderRadius.circular(10),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.grey.withOpacity(0.5),
                            spreadRadius: 5,
                            blurRadius: 7,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          // -------------------Date selector text ------------------------------
                          const SizedBox(height: 10),
                          /* Text(
                            //'Periode : ${context.watch<OrderProvider>().currentYear}',
                            // 'Période : ${context.watch<PeriodSelectorProvider>().getFormattedStartDate()} - ${context.watch<PeriodSelectorProvider>().getFormattedEndDate()}',
                            softWrap: true,
                          ),*/
                          Text(
                            '${AppLocalizations.of(context)!.turnovers_and_Profits_over_the_period}',
                            style: const TextStyle(
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                          const SizedBox(height: 10.0),
                          // ---- histogram ----
                          SizedBox(
                            height: 211,
                            child: CustomBarChart(
                              allValues: context
                                  .watch<OrderProvider>()
                                  .valueForHistogram,
                              type: 0,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 10.0),
                  // -------------------Alerts------------------------------
                  /*   Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Container(
                      width: double.infinity,
                      height: 200,
                      padding: const EdgeInsets.all(20.0),
                      decoration: BoxDecoration(
                        color: Colors.lightBlue[100],
                        borderRadius: BorderRadius.circular(10),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.grey.withOpacity(0.5),
                            spreadRadius: 5,
                            blurRadius: 7,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Text(
                            AppLocalizations.of(context)!.alerts_title,
                            style: const TextStyle(
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                              fontSize: 20,
                            ),
                          ),
                          ...lowStocks
                              .map((stock) => Padding(
                                    padding: const EdgeInsets.symmetric(
                                        vertical: 5.0),
                                    child: FlashingText(
                                      text:
                                          'Product ${stock.itemName} is low in stock with quantity ${stock.quantity}',
                                    ),
                                  ))
                              .toList(),
                        ],
                      ),
                    ),
                  ),*/
                  // -------------------sells by category ------------------------------
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Container(
                      //padding: const EdgeInsets.only(top: 20.0, ),
                      decoration: BoxDecoration(
                        color: Colors.lightBlue[100],
                        borderRadius: BorderRadius.circular(10),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.grey.withOpacity(0.5),
                            spreadRadius: 5,
                            blurRadius: 7,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              children: [
                                Text(
                                  '${AppLocalizations.of(context)!.sales_by_category_title} ',
                                  style: const TextStyle(
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 20,
                                  ),
                                ),
                                Text(
                                  '(${AppLocalizations.of(context)!.turnover_text})',
                                  style: const TextStyle(
                                    color: Colors.black,
                                    fontSize: 15,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 10),
                          SizedBox(
                            width: MediaQuery.of(context).size.width * 0.9,
                            child: ColorListChart(
                              allValues: context
                                  .watch<OrderProvider>()
                                  .valueForColorChart,
                              unity: 'CAD',
                              orderMap: true,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            );
          }
        }));
  }
}