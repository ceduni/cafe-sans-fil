import 'package:app/graph%20components/Color%20list%20chart/color_line.dart';
import 'package:flutter/material.dart';

class ColorListChart extends StatelessWidget {
  final Map<String, double> allValues;
  final String unity;

  final List<Color> allColors = [
    const Color(0xFF3498db), // Blue
    const Color(0xFF1abc9c), // Turquoise
    const Color(0xFF9b59b6), // Purple
    const Color(0xFFe74c3c), // Red
    const Color(0xFFf39c12), // Orange
    const Color(0xFF2ecc71), // Emerald
    const Color(0xFF1f8b4c), // Green
    const Color(0xFF2980b9), // Dark Blue
    const Color(0xFFd35400), // Pumpkin
    const Color(0xFF27ae60), // Nephritis
  ];

  ColorListChart({
    super.key,
    required this.allValues,
    required this.unity,
  });

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;

    return Column(
      children: [
        createLineChart(allValues, screenWidth),
        const SizedBox(height: 20),
        listOfColorLine(allValues),
        const SizedBox(height: 20),
      ],
    );
  }

  Row createLineChart(Map<String, double> allValue, double screenWidth) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: allValue.entries.toList().asMap().entries.map((entry) {
        int index = entry.key;
        double value = entry.value.value;
        double sum = allValue.values
            .fold(0, (previousValue, element) => previousValue + element);
        double resize = 0.90;
        return colorBox(
          (value * screenWidth * resize) / (sum),
          index,
        );
      }).toList(),
    );
  }

  Container colorBox(double wid, int index) {
    int colorIndex = index % allColors.length;
    return Container(
      height: 30,
      width: wid,
      color: allColors[colorIndex],
    );
  }

  Column listOfColorLine(Map<String, double> allValue) {
    return Column(
      children: allValue.entries.toList().asMap().entries.map((entry) {
        int index = entry.key;
        String name = entry.value.key;
        double value = entry.value.value;
        int colorIndex = index % allColors.length;
        double sum = allValue.values
            .fold(0, (previousValue, element) => previousValue + element);
        return ColorLine(
            name: name,
            colorCicle: allColors[colorIndex],
            value: value,
            percent: double.parse((value * 100 / sum).toStringAsFixed(2)),
            unity: unity);
      }).toList(),
    );
  }
}
