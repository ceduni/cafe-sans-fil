import 'package:app/config.dart';
import 'package:app/provider/period_selector_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class PeriodSelector extends StatefulWidget {
  const PeriodSelector({super.key});

  @override
  _PeriodSelectorState createState() => _PeriodSelectorState();
}

class _PeriodSelectorState extends State<PeriodSelector> {
  DateTime selectedStartDate = DateTime.now();
  DateTime selectedEndDate = DateTime.now();

  Future<void> _selectStartDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedStartDate,
      firstDate: DateTime(2000),
      lastDate: DateTime(3000),
    );
    if (picked != null && picked != selectedStartDate) {
      setState(() {
        context.read<PeriodSelectorProvider>().setStartDate(picked);
        selectedStartDate = picked;
      });
    }
  }

  Future<void> _selectEndDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedEndDate,
      firstDate: DateTime(2000),
      lastDate: DateTime(3000),
    );
    if (picked != null && picked != selectedStartDate) {
      setState(() {
        context.read<PeriodSelectorProvider>().setEndDate(picked);
        selectedStartDate = picked;
      });
    }
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
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        GestureDetector(
          onTap: () => _selectStartDate(context),
          child: styleButton(text: 'Debut'),
        ),
        const SizedBox(width: 5),
        GestureDetector(
          onTap: () => _selectEndDate(context),
          child: styleButton(text: 'Fin'),
        ),
      ],
    );
  }
}
