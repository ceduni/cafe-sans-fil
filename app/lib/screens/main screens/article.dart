import 'package:app/modeles/Stock.dart';
import 'package:app/provider/stock_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class Article extends StatefulWidget {
  const Article({super.key});

  @override
  State<Article> createState() => _ArticleState();
}

class _ArticleState extends State<Article> {
  Future<void> fetch() async {
    // Fetch the stocks from the database
    await Provider.of<StockProvider>(context, listen: false).fetchStock();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_articleTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: Consumer<StockProvider>(
        builder: (context, stockProvider, child) {
          if (stockProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (stockProvider.hasError) {
            return Center(child: Text('Error: ${stockProvider.errorMessage}'));
          } else {
            return Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
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
                      ],
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        // --- Menu btn ---
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color.fromARGB(255, 138, 199, 249),
                            elevation: 0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5.0),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: 12.0,
                              horizontal: 50.0,
                            ),
                          ),
                          onPressed: () {},
                          child: const Text(
                            'Menu',
                            style: TextStyle(
                              color: Colors.white,
                            ),
                          ),
                        ),
                        // --- Stock btn ---
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5.0),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: 12.0,
                              horizontal: 50.0,
                            ),
                          ),
                          onPressed: fetch,
                          child: const Text(
                            'Stock',
                            style: TextStyle(
                              color: Color.fromARGB(255, 138, 199, 249),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  Expanded(
                    child: ListView.builder(
                      itemCount: stockProvider.Stocks.length,
                      itemBuilder: (context, index) {
                        Stock stock = stockProvider.Stocks[index];
                        return ListTile(
                          title: Text(stock.itemName),
                          subtitle: Text(
                            '${AppLocalizations.of(context)!.quantity_text}: ${stock.quantity}',
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            );
          }
        },
      ),
    );
  }
}
