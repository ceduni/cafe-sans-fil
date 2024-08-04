import 'package:app/config.dart';
import 'package:app/modeles/Order%20models/Order.dart';
import 'package:app/services/orderService.dart';
import 'package:flutter/material.dart';

class OrderProvider with ChangeNotifier {
  List<Order> _Orders = [];
  String cafeName = Config.cafeName;
  double turnOver = 0.0;
  double profit = 0.0;
  List<List<double>> valueForHistogram = [];
  Map<String, double> valueForColorChart = {};
  int _currentYear = DateTime.now().year;
  bool _isLoading = false;
  String? _errorMessage;

  get Orders => _Orders;
  get isLoading => _isLoading;
  get errorMessage => _errorMessage;
  get turnOverValue => turnOver;
  get profitValue => profit;
  get currentYear => _currentYear;
  get value => valueForHistogram;
  bool get hasError => _errorMessage != null && _errorMessage!.isNotEmpty;

  OrderProvider() {
    fetchOrders();
  }

  Future<void> fetchOrders() async {
    _isLoading = true;
    try {
      _Orders = await OrderService().fetchOrders();
      turnOver = _Orders.isNotEmpty
          ? OrderService().calculateTurnOverForACafeForAYear(
              _Orders, _currentYear, cafeName)
          : 0.0;
      profit = turnOver * 0.9;
      valueForHistogram = OrderService()
          .getTurnOverAndProfitForAYear(_Orders, _currentYear, cafeName);
      valueForColorChart = OrderService()
          .getTurnOverByCategoryForACafe(_Orders, _currentYear, cafeName);
      _isLoading = false;
    } catch (e) {
      // Handle error
      _errorMessage = e.toString();
      _isLoading = false;
      print(e);
    }

    notifyListeners();
  }

  void setCurrentYear(int year) {
    if (year < 2023 || year > DateTime.now().year) {
    } else {
      _currentYear = year;
      notifyListeners();
    }
  }

  void updateHistogramData(int year) {
    valueForHistogram = OrderService()
        .getTurnOverAndProfitForAYear(_Orders, _currentYear, cafeName);
    notifyListeners();
  }

  void updateColorChartData(int year) {
    valueForColorChart = OrderService()
        .getTurnOverByCategoryForACafe(_Orders, _currentYear, cafeName);
    notifyListeners();
  }

  void updateTurnOverAndProfit(int year) {
    turnOver = OrderService()
        .calculateTurnOverForACafeForAYear(_Orders, _currentYear, cafeName);
    profit = turnOver * 0.9;
    notifyListeners();
  }
}
