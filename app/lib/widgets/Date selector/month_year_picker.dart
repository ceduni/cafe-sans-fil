import 'package:app/config.dart';
import 'package:app/provider/period_selector_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class MonthYearPicker extends StatefulWidget {
  @override
  _MonthYearPickerState createState() => _MonthYearPickerState();
}

class _MonthYearPickerState extends State<MonthYearPicker> {
  final List<String> _months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ];
  String? _selectedMonthYear;

  List<String> _generateMonthYearOptions() {
    List<int> years = [];
    for (int i = 2023; i <= DateTime.now().year; i++) {
      years.add(i);
    }
    List<String> options = [];
    for (int year in years) {
      for (String month in _months) {
        options.add('$month $year');
      }
    }
    return options;
  }

  Map<String, int> convertMonthYear(String monthYear) {
    List<String> parts = monthYear.split(' ');
    String month = parts[0];
    int year = int.parse(parts[1]);

    // Trouver le numéro du mois correspondant
    int monthIndex = _months.indexOf(month) + 1;

    return {
      'month': monthIndex,
      'year': year,
    };
  }

  Widget styleButton({required String text}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 0),
      decoration: BoxDecoration(
        color: Colors.white, // Couleur de fond du bouton
        borderRadius: BorderRadius.circular(100), // Coins arrondis
      ),
      child: Text(
        text,
        style: TextStyle(
          color: Config.specialBlue, // Couleur du texte
          fontSize: 14,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    List<String> monthYearOptions = _generateMonthYearOptions();

    return Row(
      children: [
        DropdownButton<String>(
          hint: const Text('month year'),
          value: _selectedMonthYear,
          onChanged: (String? newValue) {
            Map<String, int> monthYear = convertMonthYear(newValue!);
            int? month = monthYear['month'];
            int? year = monthYear['year'];
            setState(() {
              _selectedMonthYear = newValue;
              if (month != null && year != null) {
                context.read<PeriodSelectorProvider>().setMonthPicked(month);
                context.read<PeriodSelectorProvider>().setYearPicked(year);
              }
            });
          },
          items: monthYearOptions.map<DropdownMenuItem<String>>((String value) {
            return DropdownMenuItem<String>(
              value: value,
              child: styleButton(text: value),
            );
          }).toList(),
        ),
      ],
    );
  }
}
