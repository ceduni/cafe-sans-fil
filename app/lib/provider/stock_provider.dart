import 'package:app/config.dart';
import 'package:app/modeles/Stock.dart';
import 'package:app/services/StockService.dart';
import 'package:flutter/material.dart';

class StockProvider with ChangeNotifier {
  List<Stock> _Stocks = [];
  List<String> lowStockProcductName = [];

  String cafeName = Config.cafeName;
  bool _isLoading = false;
  String? _errorMessage;

  get Stocks => _Stocks;
  get isLoading => _isLoading;
  get errorMessage => _errorMessage;
  bool get hasError => _errorMessage != null && _errorMessage!.isNotEmpty;
  List<String> get lowStockProcductNameList => lowStockProcductName;

  StockProvider() {
    fetchStock();
  }

  Future<void> fetchStock() async {
    _isLoading = true;
    try {
      _Stocks = await StockService().fetchStocks();
      lowStockProcductName = StockService().getLowStocksProductsNames(_Stocks);
      _isLoading = false;
    } catch (e) {
      // Handle error
      _errorMessage = e.toString();
      _isLoading = false;
      print(e);
    }

    notifyListeners();
  }
}
