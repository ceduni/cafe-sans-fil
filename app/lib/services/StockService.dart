import 'dart:convert';

import 'package:app/modeles/Stock.dart';
import 'package:http/http.dart' as http;

class StockService {
  final String baseUrl = "http://Localhost:3000/api/v1/stock";

  StockService({dynamic});

  Future<List<Stock>> getStocks() async {
    var url = Uri.parse(baseUrl);
    var response = await http.get(url);

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
}

void main() async {
  var stockService = new StockService();
  List<Stock> stocks = await stockService.getStocks();
  print(stocks);
  List<Stock> lowStocks = Stock.lowQuantity(stocks);
  print(lowStocks);
}
