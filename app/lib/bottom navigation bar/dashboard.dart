import 'package:app/graph%20components/Color%20list%20chart/color_list_chart.dart';
import 'package:app/graph%20components/financial_data_row.dart';
import 'package:app/graph%20components/histogram/custom_bar_chart.dart';
import 'package:app/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        drawer: const Sidebar(),
        appBar: AppBar(
          title: Text(AppLocalizations.of(context)!.pagesTitles_dashboardTitle),
          surfaceTintColor: Colors.blue,
        ),
        body: SingleChildScrollView(
          child: Column(
            children: [
              /* Center(
                child: ClipRect(
                  child: SizedBox(
                    height: 150,
                    width: 150,
                    child: Image.asset(
                      'images/ToreFractionLogo.jpg',
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
              ),*/
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
                          fontSize: 18.0,
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10.0),
                      const Text(
                        '1395.78 CAD',
                        style: TextStyle(
                          fontSize: 20.0,
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      )
                    ],
                  ),
                  const SizedBox(width: 70.0),
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        AppLocalizations.of(context)!.sales_numbers_text,
                        style: const TextStyle(
                          fontSize: 18.0,
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 10.0),
                      const Text(
                        '129',
                        style: TextStyle(
                          fontSize: 20.0,
                          color: Colors.black,
                          fontWeight: FontWeight.bold,
                        ),
                      )
                    ],
                  )
                ],
              ),
              const SizedBox(height: 30.0),
              Container(
                //sell's evolution title
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
                // period selector
                alignment: Alignment.topLeft,
                width: 300,
                height: 30,
                decoration: BoxDecoration(
                  color: Colors.blue,
                  borderRadius: BorderRadius.circular(30),
                ),
                child: const Padding(
                  padding: EdgeInsets.all(5),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Choisir période',
                      style: TextStyle(color: Colors.white),
                    ),
                  ),
                ),
              ),
              const SizedBox(
                height: 35.0,
              ),
              const SizedBox(
                // Histogram
                width: 350,
                height: 200,
                child: CustomBarChart(
                  allValues: [
                    [150.0, 400.0],
                    [234.0, 345.0],
                    [150.0, 400.0],
                    [234.0, 345.0],
                    [234.0, 375.0],
                    [234.0, 505.0],
                    [234.0, 345.0],
                  ],
                  type: 0,
                ),
              ),
              const SizedBox(
                height: 20,
              ),
              Column(
                children: [
                  FinancialDataRow(
                    title: AppLocalizations.of(context)!
                        .turnover_over_the_period_text,
                    value: '999,59 CAD ',
                  ),
                  FinancialDataRow(
                    title: AppLocalizations.of(context)!
                        .profits_over_the_period_text,
                    value: '123500,34 CAD ',
                  ),
                ],
              ),
              Container(
                //Alerts titles
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
                //Alerts zone
                width: 350,
                height: 200,
                decoration: BoxDecoration(
                  color: Colors.blue,
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              Container(
                //sells by category title
                padding: const EdgeInsets.all(20.0),
                alignment: Alignment.topLeft,
                child: Text(
                  ' ${AppLocalizations.of(context)!.profits_over_the_period_text} (${AppLocalizations.of(context)!.turnover_text})',
                  style: const TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                  ),
                ),
              ),
              Column(children: [
                ColorListChart(
                  allValues: const {
                    'lait': 395000,
                    'pain': 300070,
                    'hot-dog': 343222,
                    'pizza': 450000,
                    'burger': 389900
                  },
                  unity: 'CAD',
                ),
              ]),
            ],
          ),
        ));
  }
}
