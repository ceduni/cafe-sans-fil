import 'dart:convert';

import 'package:app/config.dart';
import 'package:app/modeles/Stock.dart';
import 'package:app/widgets/FlashMessage.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class StockService {
  final String baseUrl = "${Config.baseUrl}/stocks";

  StockService({dynamic});

  Future<List<Stock>> fetchStocks() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url).timeout(const Duration(seconds: 25));

    if (response.statusCode == 200) {
      var jsonData = json.decode(response.body);

      if (jsonData['Stock'] != null) {
        List<dynamic> stocksJson = jsonData['Stock'];
        List<Stock> stocks =
            stocksJson.map((json) => Stock.fromJson(json)).toList();
        return stocks;
      } else {
        throw Exception('Stock data is not available');
      }
    } else {
      throw Exception('Failed to load stock from $baseUrl');
    }
  }

  List<String> getLowStocksProductsNames(List<Stock> stocks) {
    List<String> alerts = [];

    for (Stock stock in stocks) {
      // Example condition for low stock
      if (stock.quantity < 10) {
        String alert = stock.itemName;
        alerts.add(alert);
      }
    }
    return alerts;
  }

/*
void main() async {
  var stockService = new StockService();
  List<Stock> stocks = await stockService.fetchStocks();
  print(stocks);
  List<Stock> lowStocks = Stock.lowQuantity(stocks);
  print(lowStocks);
}
*/

  void checkProductQuantities(List<Stock> lowStocks, BuildContext context) {
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
}
