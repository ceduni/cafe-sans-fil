import 'package:flutter/material.dart';

class ColorLine extends StatelessWidget {
  final Color colorCicle;
  final double value;
  final double percent;
  final String unity;
  final String name;

  const ColorLine(
      {super.key,
      required this.colorCicle,
      required this.value,
      required this.percent,
      required this.unity,
      required this.name});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        SizedBox(width: screenWidth / 100),
        Container(
          height: 18,
          width: 18,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: colorCicle,
          ),
          child: Center(
            child: Container(
              height: 8,
              width: 8,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white,
              ),
            ),
          ),
        ),
        const SizedBox(width: 5),
        Container(
          width: screenWidth / 2.7,
          alignment: Alignment.centerLeft,
          child: Text(
            '$name ',
            style: const TextStyle(
              fontSize: 16.0,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        Container(
          width: screenWidth / 2.3,
          alignment: Alignment.centerLeft,
          padding: const EdgeInsets.only(left: 15),
          child: Text(
            '${value.toStringAsFixed(2)} $unity ($percent %)',
            style: const TextStyle(
              fontSize: 15.4,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        const SizedBox(height: 35),
      ],
    );
  }
}
