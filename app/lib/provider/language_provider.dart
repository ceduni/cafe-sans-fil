import 'package:flutter/material.dart';

class LanguageProvider extends ChangeNotifier {
  Locale _actualLanguage = const Locale("fr", "FR");

  Locale getactualLanguage() => _actualLanguage;

  void changeLanguague({required Locale newLanguage}) async {
    _actualLanguage = newLanguage;
    notifyListeners();
  }
}
