import 'dart:ffi';

import 'package:app/modeles/Order%20models/Order.dart';
import 'package:app/modeles/Stock.dart';
import 'package:app/provider/order_provider.dart';
import 'package:app/screens/main screens/FlashMessage.dart';
import 'package:app/screens/main%20screens/FlashingText.dart';
import 'package:app/services/stockService.dart';
import 'package:app/provider/period_selector_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/services/productService.dart';
import 'package:app/widgets/Color%20list%20chart/color_list_chart.dart';
import 'package:app/widgets/histogram/custom_bar_chart.dart';
import 'package:app/widgets/period_selector.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

//import 'flash_message.dart'; // Import the FlashMessage widget

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class NotificationItem {
  final String title;
  final String subtitle;

  NotificationItem(this.title, this.subtitle);
}

class _DashboardState extends State<Dashboard> {
  final ProductService productService = ProductService();
  final StockService stockService = StockService();
  List<Stock> lowStocks = [];
  List<Stock> stocks = [];
  Map<String, dynamic> revenueByCategory = {};
  List<Order> orders = [];
  bool isLoading = true;
  double turnOver = 0.0;
  int salesNumbers = 0;
  @override
  void initState() {
    super.initState();
    fetch();
  }

  Future<void> fetch() async {
    await Provider.of<OrderProvider>(context, listen: false).fetchOrders();

    try {
      List<Order> fetchedOrders = await productService.fetchOrders();
      print("Fetched orders: ${fetchedOrders.length}");
      stocks = await stockService.getStocks();
      print("Fetched stocks: ${stocks.length}");
      revenueByCategory = Order.revenueByCategory(fetchedOrders, stocks);

      setState(() {
        orders = fetchedOrders;
        turnOver = Order.turnOver(orders, startDate: 'date', endDate: 'Date');
        print(turnOver);
        salesNumbers = Order.numOfOrder(orders);
        lowStocks = Stock.lowQuantity(stocks);

        isLoading = false;
      });

      // Show flash message if product quantity is low
      checkProductQuantities();
    } catch (error) {
      setState(() {
        isLoading = false;
      });
    }
  }

  void checkProductQuantities() {
    for (Stock stock in lowStocks) {
      // Example condition for low stock
      showFlashMessage(context,
          'Le Product ${stock.itemName} a une quantite faible en stock!');
    }
  }

  void showFlashMessage(BuildContext context, String message) {
    OverlayState? overlayState = Overlay.of(context);
    OverlayEntry overlayEntry = OverlayEntry(
      builder: (context) => Positioned(
        top: 50,
        left: 0,
        right: 0,
        child: Material(
          color: Colors.transparent,
          child: FlashMessage(message: message),
        ),
      ),
    );

    overlayState.insert(overlayEntry);

    // Remove the flash message after 3 seconds
    Future.delayed(const Duration(seconds: 5), () {
      overlayEntry.remove();
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
        body: Consumer<OrderProvider>(builder: (context, orderProvider, child) {
          if (orderProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (orderProvider.hasError) {
            return Center(child: Text('Error: ${orderProvider.errorMessage}'));
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
                  // ----------- logo ------------
                  Container(
                    padding: const EdgeInsets.all(16.0),
                    child: PopupMenuButton<NotificationItem>(
                      onSelected: (NotificationItem result) {
                        // Action à effectuer lors de la sélection d'un élément
                        print('Selected: ${result.title}');
                      },
                      itemBuilder: (BuildContext context) =>
                          <PopupMenuEntry<NotificationItem>>[
                        PopupMenuItem<NotificationItem>(
                          value: NotificationItem(
                              'Notification 1', 'You have a new message'),
                          child: const ListTile(
                            leading: Icon(Icons.message),
                            title: Text('Notification 1'),
                            subtitle: Text('You have a new message'),
                          ),
                        ),
                        PopupMenuItem<NotificationItem>(
                          value: NotificationItem(
                              'Notification 2', 'Your order has been shipped'),
                          child: const ListTile(
                            leading: Icon(Icons.local_shipping),
                            title: Text('Notification 2'),
                            subtitle: Text('Your order has been shipped'),
                          ),
                        ),
                        PopupMenuItem<NotificationItem>(
                          value: NotificationItem(
                              'Notification 3', 'Update available'),
                          child: const ListTile(
                            leading: Icon(Icons.update),
                            title: Text('Notification 3'),
                            subtitle: Text('Update available'),
                          ),
                        ),
                      ],
                      icon: Icon(Icons.notifications),
                    ),
                  ),

                  const SizedBox(height: 20.0),
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
                                // -- turnover --
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
                                  AppLocalizations.of(context)!
                                      .profits_over_the_period_text,
                                  style: const TextStyle(
                                    fontSize: 15,
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold,
                                  ),
                                  softWrap: true,
                                ),
                                const SizedBox(height: 10.0),
                                // -- profit --
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
                        PeriodSelector(),
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
                          Text(
                            'Période : ${context.watch<PeriodSelectorProvider>().getFormattedStartDate()} - ${context.watch<PeriodSelectorProvider>().getFormattedEndDate()}',
                            softWrap: true,
                          ),
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
                            height: MediaQuery.of(context).size.height * 0.3,
                            width: MediaQuery.of(context).size.width * 0.9,
                            child: ColorListChart(
                              allValues: context
                                  .watch<OrderProvider>()
                                  .valueForColorChart,
                              unity: 'CAD',
                              orderMap: false,
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
