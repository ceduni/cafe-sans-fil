import 'dart:ffi';

import 'package:app/modeles/Order%20models/Order.dart';
import 'package:app/services/orderService.dart';
import 'package:flutter/material.dart';

class OrderProvider with ChangeNotifier {
  List<Order> _Orders = [];
  double turnOver = 0.0;
  double profit = 0.0;
  List<List<double>> valueForHistogram = [];
  Map<String, double> valueForColorChart = {};
  int _currentYear = 2024;
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
          ? OrderService()
              .calculateTurnOverForACafeAllTime(_Orders, "Bauch - Pacocha")
          : 0.0;
      profit = turnOver - 500.0;
      valueForHistogram = OrderService().getTurnOverAndProfitForAYear(
          _Orders, _currentYear, "Bauch - Pacocha");
      valueForColorChart = OrderService().getTurnOverByCategoryForACafe(
          _Orders, _currentYear, "Bauch - Pacocha");
      _isLoading = false;
    } catch (e) {
      // Handle error
      _errorMessage = e.toString();
      _isLoading = false;
      print(e);
    }

    notifyListeners();
  }

  void setYearForHistogram(int year) {
    if (year < 2019 || year > DateTime.now().year) {
    } else {
      _currentYear = year;
      notifyListeners();
    }
  }
}
