import 'package:app/modeles/Stock.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/services/StockService.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class Article extends StatefulWidget {
  const Article({super.key});

  @override
  State<Article> createState() => _ArticleState();
}

class _ArticleState extends State<Article> {
  List<Stock> stocks = [];
  StockService stockService = StockService();

  Future<void> fetch() async {
    // Fetch the stocks from the database
    try {
      List<Stock> stock = await stockService.fetchStocks();
      setState(() {
        stocks = stock;
      });
    } catch (e) {
      // ignore: avoid_print
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_articleTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            Container(
              padding: const EdgeInsets.all(20.0),
              decoration: BoxDecoration(
                  color: const Color.fromARGB(255, 138, 199, 249),
                  borderRadius: BorderRadius.circular(10.0),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.5),
                      spreadRadius: 2,
                      blurRadius: 7,
                      offset: const Offset(0, 3),
                    ),
                  ]),
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    // --- Menu btn ---
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor:
                            const Color.fromARGB(255, 138, 199, 249),
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(5.0),
                        ),
                        padding: const EdgeInsets.only(
                            top: 12, bottom: 12.0, left: 50.0, right: 50.0),
                      ),
                      onPressed: () {},
                      child: const Text('Menu',
                          style: TextStyle(
                            color: Colors.white,
                          )),
                    )
                    // -- stock btn --
                    ,
                    ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(5.0),
                          ),
                          padding: const EdgeInsets.only(
                              top: 12, bottom: 12.0, left: 50.0, right: 50.0),
                        ),
                        onPressed: () {
                          fetch();
                        },
                        child: const Text(
                          'Stock',
                          style: TextStyle(
                            color: Color.fromARGB(255, 138, 199, 249),
                          ),
                        ))
                  ]),
            ),
            const SizedBox(height: 20),
            ListView.builder(
              shrinkWrap: true,
              itemCount: stocks.length,
              itemBuilder: (context, index) {
                Stock stock = stocks[index];
                return ListTile(
                  title: Text(stock.itemName),
                  subtitle: Text('Quantity: ${stock.quantity}'),
                );
              },
            )
          ],
        ),
      ),
    );
  }
}
