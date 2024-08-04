import 'package:app/config.dart';
import 'package:app/provider/order_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class YearPickerWidget extends StatefulWidget {
  final int initialYear = DateTime.now().year;
  final int firstYear = 2023;
  final int lastYear = DateTime.now().year;

  YearPickerWidget();

  @override
  _YearPickerWidgetState createState() => _YearPickerWidgetState();
}

class _YearPickerWidgetState extends State<YearPickerWidget> {
  int? _selectedYear;

  @override
  void initState() {
    super.initState();
    _selectedYear = DateTime.now().year;
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
    return GestureDetector(
      onTap: () async {
        final DateTime? picked = await showDatePicker(
          context: context,
          initialDate: DateTime(_selectedYear!),
          firstDate: DateTime(widget.firstYear),
          lastDate: DateTime(widget.lastYear),
          initialDatePickerMode: DatePickerMode.year,
        );

        if (picked != null && picked.year != _selectedYear) {
          setState(() {
            _selectedYear = picked.year;
            context.read<OrderProvider>().setCurrentYear(picked.year);
            context.read<OrderProvider>().updateHistogramData(picked.year);
            context.read<OrderProvider>().updateColorChartData(picked.year);
            context.read<OrderProvider>().updateTurnOverAndProfit(picked.year);
          });
        }
      },
      child: styleButton(text: '${_selectedYear!}'),
    );
  }
}
