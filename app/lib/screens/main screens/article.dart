import 'package:app/config.dart';
import 'package:app/modeles/Cafe.dart';
import 'package:app/modeles/Stock.dart';
import 'package:app/provider/cafe_provider.dart';
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
  bool isButtonASelected = true;

  void initState() {
    super.initState();
    fetch();
  }

  Future<void> fetch() async {
    // Fetch the stocks from the database
    await Provider.of<StockProvider>(context, listen: false).fetchStock();
    if (!mounted) return;

    await Provider.of<CafeProvider>(context, listen: false).fetchCafe();
    if (!mounted) return;
  }

  ListView stockList(List<Stock> stocks) {
    return ListView.builder(
      itemCount: stocks.length,
      itemBuilder: (context, index) {
        Stock stock = stocks[index];
        return ListTile(
          title: Text(stock.itemName),
          subtitle: Text(
            '${AppLocalizations.of(context)!.quantity_text}: ${stock.quantity}',
          ),
        );
      },
    );
  }

  ListView ItemMenuList(List<MenuItem> menuItems) {
    return ListView.builder(
      itemCount: menuItems.length,
      itemBuilder: (context, index) {
        MenuItem menuItem = menuItems[index];
        return ListTile(
          leading: menuItem.imageUrl.isNotEmpty
              ? Image.network(
                  menuItem.imageUrl,
                  width: 50, // Ajustez la largeur selon vos besoins
                  height: 50, // Ajustez la hauteur selon vos besoins
                  fit: BoxFit.cover, // Ajustez le fit pour bien adapter l'image
                  loadingBuilder: (BuildContext context, Widget child,
                      ImageChunkEvent? loadingProgress) {
                    if (loadingProgress == null) {
                      return child;
                    } else {
                      return SizedBox(
                        width: 50,
                        height: 50,
                        child: Center(
                          child: CircularProgressIndicator(
                            color: Config.specialBlue,
                            value: loadingProgress.expectedTotalBytes != null
                                ? loadingProgress.cumulativeBytesLoaded /
                                    (loadingProgress.expectedTotalBytes ?? 1)
                                : null,
                          ),
                        ),
                      );
                    }
                  },
                  errorBuilder: (BuildContext context, Object error,
                      StackTrace? stackTrace) {
                    return const Icon(Icons.broken_image);
                  },
                )
              : const Icon(Icons.image_not_supported),
          title: Text(menuItem.name),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_articleTitle),
        surfaceTintColor: Config.specialBlue,
      ),
      body: Consumer2<StockProvider, CafeProvider>(
        builder: (context, stockProvider, cafeProvider, child) {
          if (stockProvider.isLoading || cafeProvider.isLoading) {
            return Center(
                child: CircularProgressIndicator(color: Config.specialBlue));
          } else if (stockProvider.hasError || cafeProvider.hasError) {
            return Center(
                child: Text(
                    'Error: ${stockProvider.errorMessage ?? cafeProvider.errorMessage}'));
          } else {
            return Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    decoration: BoxDecoration(
                      color: Config.specialBlue,
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
                            elevation: isButtonASelected ? 5 : 0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5.0),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: 12.0,
                              horizontal: 50.0,
                            ),
                            backgroundColor: isButtonASelected
                                ? Colors.white
                                : Config.specialBlue,
                          ),
                          onPressed: () {
                            setState(() {
                              isButtonASelected = true;
                            });
                          },
                          child: Text('Menu',
                              style: TextStyle(
                                  color: isButtonASelected
                                      ? Config.specialBlue
                                      : Colors.white)),
                        ),
                        // --- Stock btn ---
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            elevation: isButtonASelected ? 0 : 5,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5.0),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: 12.0,
                              horizontal: 50.0,
                            ),
                            backgroundColor: isButtonASelected
                                ? Config.specialBlue
                                : Colors.white,
                          ),
                          onPressed: () {
                            setState(() {
                              isButtonASelected = false;
                            });
                          },
                          child: Text(
                            'Stock',
                            style: TextStyle(
                                color: isButtonASelected
                                    ? Colors.white
                                    : Config.specialBlue),
                          ),
                        )
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),
                  Expanded(
                    child: isButtonASelected
                        ? ItemMenuList(cafeProvider.getMenuItems)
                        : stockList(stockProvider.Stocks),
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
