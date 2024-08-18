import 'package:flutter/material.dart';

class SettingProvider extends ChangeNotifier {
  Locale _actualLanguage = const Locale("fr", "FR");
  Color specialColor = const Color.fromARGB(255, 138, 199, 249);
  Color specialColorLight = Colors.lightBlue[100]!;
  Color BackgroundColor = Colors.white;

  Locale getactualLanguage() => _actualLanguage;
  Color getSpecialColor() => specialColor;
  Color getSpecialColorLight() => specialColorLight;
  Color getBackgroundColor() => BackgroundColor;

  void changeLanguague({required Locale newLanguage}) async {
    _actualLanguage = newLanguage;
    notifyListeners();
  }

  void changeColorYellowBackgroundBlack() {
    specialColor = Colors.amber;
    specialColorLight = Colors.yellow[200]!;
    BackgroundColor = Colors.black;
    notifyListeners();
  }

  void changeColorBlueBackgroundWhite() {
    specialColor = const Color.fromARGB(255, 138, 199, 249);
    specialColorLight = Colors.lightBlue[100]!;
    BackgroundColor = Colors.white;
    notifyListeners();
  }
}
