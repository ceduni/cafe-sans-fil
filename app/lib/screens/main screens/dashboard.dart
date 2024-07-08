import 'package:app/modeles/Order.dart';
import 'package:app/provider/period_selector_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/services/productService.dart';
import 'package:app/widgets/Color%20list%20chart/color_list_chart.dart';
import 'package:app/widgets/financial_data_row.dart';
import 'package:app/widgets/histogram/custom_bar_chart.dart';
import 'package:app/widgets/period_selector.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  bool isLoading = true;
  List<Order> orders = [];
  // Turnover for the sales months 
  double janTurnOver = 0.0;
  double febTurnOver = 0.0;
  double marTurnOver = 0.0;
  double aprTurnOver = 0.0;
  double mayTurnOver = 0.0;
  double junTurnOver = 0.0;
  double julTurnOver = 0.0;
  double augTurnOver = 0.0;

  // Months profit variables
  double janProfit = 0.0;
  double febProfit = 0.0;
  double marProfit = 0.0;
  double aprProfit = 0.0;
  double mayProfit = 0.0;
  double junProfit = 0.0;
  double julProfit = 0.0;
  double augProfit = 0.0;

  final ProductService productService = ProductService();
  double turnOver = 0.0;
  int salesNumbers = 0;

  @override
  void initState() {
    super.initState();
    fetchOrders();
    calculateTurnOverAndProfit();
  }

  Future<void> fetchOrders() async {
    try {
      List<Order> fetchedOrders = await productService.fetchOrders();
      setState(() {
        orders = fetchedOrders;
        turnOver = Order.turnOver(orders);
        salesNumbers = Order.numOfOrder(orders);
        isLoading = false;
        calculateTurnOverAndProfit();
      });
    } catch (error) {
      setState(() {
        isLoading = false;
      });
    }
  }

  void calculateTurnOverAndProfit() {
    setState(() {
      janTurnOver = Order.turnOverDate(orders, 1);
      febTurnOver = Order.turnOverDate(orders, 2);
      marTurnOver = Order.turnOverDate(orders, 3);
      aprTurnOver = Order.turnOverDate(orders, 4);
      mayTurnOver = Order.turnOverDate(orders, 5);
      junTurnOver = Order.turnOverDate(orders, 6);
      julTurnOver = Order.turnOverDate(orders, 7);
      augTurnOver = Order.turnOverDate(orders, 8);

      janProfit = Order.calculateProfit(janTurnOver);
      print(janProfit);
      febProfit = Order.calculateProfit(febTurnOver);
      print(febProfit);
      marProfit = Order.calculateProfit(marTurnOver);
      aprProfit = Order.calculateProfit(aprTurnOver);
      mayProfit = Order.calculateProfit(mayTurnOver);
      junProfit = Order.calculateProfit(junTurnOver);
      julProfit = Order.calculateProfit(julTurnOver);
      augProfit = Order.calculateProfit(augTurnOver);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_dashboardTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              child: Column(
                children: [
                  Center(
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
                  const SizedBox(height: 30.0),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            AppLocalizations.of(context)!.turnover_text,
                            style: const TextStyle(
                              fontSize: 20.0,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 10.0),
                          Text(
                            '${turnOver.toStringAsFixed(2)} CAD',
                            style: const TextStyle(
                              fontSize: 20.0,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(width: 40.0),
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            AppLocalizations.of(context)!.sales_numbers_text,
                            style: const TextStyle(
                              fontSize: 20,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 10.0),
                          Text(
                            '$salesNumbers',
                            style: const TextStyle(
                              fontSize: 20.0,
                              color: Colors.black,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 30.0),
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    alignment: Alignment.topLeft,
                    child: Text(
                      AppLocalizations.of(context)!.evolution_of_sales_title,
                      style: const TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                      ),
                    ),
                  ),
                  Container(
                    alignment: Alignment.center,
                    width: 300,
                    height: 30,
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
                        const PeriodSelector(),
                      ],
                    ),
                  ),
                  Text(
                    'Période : ${context.watch<PeriodSelectorProvider>().getFormattedStartDate()} - ${context.watch<PeriodSelectorProvider>().getFormattedEndDate()}',
                  ),
                  const SizedBox(height: 35.0),
                  SizedBox(
                    width: 350,
                    height: 200,
                    child: CustomBarChart(
                      allValues: [
                        [janProfit, janTurnOver],
                        [febProfit, febTurnOver],
                        [marProfit, marTurnOver],
                        [aprProfit, aprTurnOver],
                        [mayProfit, mayTurnOver],
                        [junProfit, junTurnOver],
                        [julProfit, julTurnOver],
                        [augProfit, augTurnOver],
                      ],
                      type: 0,
                    ),
                  ),
                  const SizedBox(height: 20),
                  Column(
                    children: [
                      FinancialDataRow(
                        title: AppLocalizations.of(context)!
                            .turnover_over_the_period_text,
                        value:
                            '${Order.turnOver(orders, startDate: context.watch<PeriodSelectorProvider>().getFormattedStartDate(), endDate: context.watch<PeriodSelectorProvider>().getFormattedEndDate()).toStringAsFixed(2)} CAD',
                      ),
                      FinancialDataRow(
                        title: AppLocalizations.of(context)!
                            .profits_over_the_period_text,
                        value:
                            '${Order.calculateProfit(Order.turnOver(orders, startDate: context.watch<PeriodSelectorProvider>().getFormattedStartDate(), endDate: context.watch<PeriodSelectorProvider>().getFormattedEndDate()))}',
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    alignment: Alignment.topLeft,
                    child: Text(
                      AppLocalizations.of(context)!.alerts_title,
                      style: const TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                      ),
                    ),
                  ),
                  Container(
                    width: 350,
                    height: 200,
                    decoration: BoxDecoration(
                      color: const Color.fromARGB(255, 138, 199, 249),
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    alignment: Alignment.topLeft,
                    child: Text(
                      '${AppLocalizations.of(context)!.sales_by_category_title} (${AppLocalizations.of(context)!.turnover_text})',
                      style: const TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                      ),
                    ),
                  ),
                  ColorListChart(
                    allValues: const {
                      'lait': 39500,
                      'pain': 300070,
                      'hot-dog': 343222,
                      'pizza': 450000,
                    },
                    unity: 'CAD',
                    orderMap: false,
                  ),
                ],
              ),
            ),
    );
  }
}
