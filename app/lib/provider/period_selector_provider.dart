import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class PeriodSelectorProvider extends ChangeNotifier {
  DateTime _selectedStartDate =
      DateTime.now().subtract(const Duration(days: 1));
  DateTime _selectedEndDate = DateTime.now();

  int _monthPicked = DateTime.now().month;
  int _yearPicked = DateTime.now().year;

  PeriodSelectorProvider();

  DateTime get selectedStartDate => _selectedStartDate;
  DateTime get selectedEndDate => _selectedEndDate;

  int get monthPicked => _monthPicked;
  int get yearPicked => _yearPicked;

  void setMonthPicked(int month) {
    _monthPicked = month;
    notifyListeners();
  }

  void setYearPicked(int year) {
    _yearPicked = year;
    notifyListeners();
  }

  void setStartDate(DateTime date) {
    if (date.isBefore(_selectedEndDate)) {
      _selectedStartDate = date;
    }
    notifyListeners();
  }

  void setEndDate(DateTime date) {
    if (date.isAfter(_selectedStartDate)) {
      _selectedEndDate = date;
    }
    notifyListeners();
  }

  void setPeriod(DateTime startDate, DateTime endDate) {
    _selectedStartDate = startDate;
    _selectedEndDate = endDate;
    notifyListeners();
  }

  String getFormattedStartDate() {
    return DateFormat('dd/MM/yyyy').format(_selectedStartDate);
  }

  String getFormattedEndDate() {
    return DateFormat('dd/MM/yyyy').format(_selectedEndDate);
  }
}
