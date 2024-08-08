import 'package:flutter/material.dart';

class HistogramLegend extends StatelessWidget {
  final String title;
  final Color color;
  HistogramLegend({super.key, required this.title, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          height: 10,
          width: 10,
          color: color,
        ),
        const SizedBox(
          width: 10,
        ),
        Text(
          title,
          style: const TextStyle(
            fontSize: 15.0,
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
          softWrap: true,
        ),
      ],
    );
  }
}
