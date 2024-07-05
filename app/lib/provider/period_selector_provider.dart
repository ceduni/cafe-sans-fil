import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class PeriodSelectorProvider extends ChangeNotifier {
  DateTime _selectedStartDate;
  DateTime _selectedEndDate;

  PeriodSelectorProvider({
    DateTime? selectedStartDate,
    DateTime? selectedEndDate,
  })  : _selectedStartDate = selectedStartDate ?? DateTime.now(),
        _selectedEndDate = selectedEndDate ?? DateTime.now();

  DateTime get selectedStartDate => _selectedStartDate;
  DateTime get selectedEndDate => _selectedEndDate;

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
