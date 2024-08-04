import 'package:app/config.dart';
import 'package:app/modeles/Cafe.dart';
import 'package:app/services/CafeService.dart';
import 'package:flutter/material.dart';

class CafeProvider with ChangeNotifier {
  String cafeName = Config.cafeName;
  bool _isLoading = false;
  String? _errorMessage;
  var _Cafe;

  get Cafe => _Cafe;
  get isLoading => _isLoading;
  get errorMessage => _errorMessage;
  bool get hasError => _errorMessage != null && _errorMessage!.isNotEmpty;

  CafeProvider() {
    fetchCafe();
  }

  List<MenuItem> get getMenuItems => _Cafe?.menuItems ?? [];

  Future<void> fetchCafe() async {
    _isLoading = true;
    try {
      _Cafe = await CafeService().fetchCafeByName(cafeName);

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
