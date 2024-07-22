import 'package:app/provider/period_selector_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class YearPickerCustom extends StatefulWidget {
  @override
  _YearPickerCustomState createState() => _YearPickerCustomState();
}

class _YearPickerCustomState extends State<YearPickerCustom> {
  String? _selectedYear;

  List<String> _generateYearOptions() {
    List<int> years = [];
    for (int i = 2019; i <= DateTime.now().year; i++) {
      years.add(i);
    }
    List<String> options = [];
    for (int year in years) {
      options.add('$year');
    }
    return options;
  }

  int convertYear(String Year) {
    int year = int.parse(Year);
    return year;
  }

  Widget styleButton({required String text}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 2),
      decoration: BoxDecoration(
        color: Colors.white, // Couleur de fond du bouton
        borderRadius: BorderRadius.circular(100), // Coins arrondis
      ),
      child: Text(
        text,
        style: const TextStyle(
          color: Color.fromARGB(255, 138, 199, 249), // Couleur du texte
          fontSize: 14,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    List<String> YearOptions = _generateYearOptions();

    return DropdownButton<String>(
      hint: const Text('Year'),
      value: _selectedYear,
      onChanged: (String? newValue) {
        setState(() {
          _selectedYear = newValue;
          int? year = convertYear(newValue!);
          context.read<PeriodSelectorProvider>().setYearPicked(year);
        });
      },
      items: YearOptions.map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: styleButton(text: value),
        );
      }).toList(),
    );
  }
}
