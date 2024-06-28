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
      children: [
        const SizedBox(width: 40),
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
        const SizedBox(width: 10),
        Row(
          children: [
            Container(
              width: screenWidth / 3,
              alignment: Alignment.centerLeft,
              child: Text(
                '$name ',
                style: const TextStyle(
                  fontSize: 16.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(width: 10),
            Container(
              alignment: Alignment.centerLeft,
              child: Text(
                '$value $unity ($percent %)',
                style: const TextStyle(
                  fontSize: 16.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 35),
      ],
    );
  }
}
